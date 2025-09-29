from django.db import transaction
from rest_framework import serializers
from .models import Usuario, Rol, RolUsuario, Personal, Residente
from unidades.models import UnidadHabitacional, ResidenteUnidad

from django.core.mail import send_mail

# AÑADI ESTO NUEVO: Se agregó el serializador PersonalReadSerializer para las operaciones de lectura de perfiles de personal.

# ---------------------------------------------
# Funciones utilitarias
# ---------------------------------------------
def send_credentials_email(user_email, username, temp_password):
    """Envía un email con las credenciales de acceso."""
    try:
        # Nota: La contraseña aquí es la de texto plano que el Admin ingresó
        send_mail(
            "Credenciales de Acceso a la Plataforma",
            (
                f"Hola {username},\n\n"
                f"Tu cuenta ha sido registrada por el administrador. Usa las siguientes credenciales para iniciar sesión:\n"
                f"Username: {username}\n"
                f"Contraseña: {temp_password}\n\n"
                f"Por favor, cambia tu contraseña al iniciar sesión por primera vez.\n\n"
                f"Atentamente,\nEl Equipo de SmartCondo"
            ),
            "no-reply@smartcondo.app", # Remitente
            [user_email], 
            fail_silently=True, # Deja esto en True si tienes problemas de configuración de SMTP en Railway
        )
    except Exception as e:
        # Esto imprimirá el error en tu consola si falla el envío
        print(f"ERROR: No se pudo enviar el correo a {user_email}. {e}")


# -----------------------------
# Serializer de Roles
# -----------------------------
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ["id", "nombre"]


# -----------------------------
# Usuario - Read
# -----------------------------
class UsuarioReadSerializer(serializers.ModelSerializer):
    roles = RolSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "ci", "nombre", "telefono", "estado", "url_img",
            "registro_facial", "carnet", "roles"
        ]


# -----------------------------
# Usuario - Write
# -----------------------------
class UsuarioWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "id", "username", "password", "email", "first_name",
            "last_name", "ci", "nombre", "telefono", "estado",
            "url_img", "registro_facial", "carnet"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        # Usa create_user para normalizar comportamiento (hash, etc.)
        user = Usuario.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user


# -----------------------------
# Personal - Create
# Crea Usuario + asigna rol PERSONAL + crea Personal
# -----------------------------
class PersonalCreateSerializer(serializers.ModelSerializer):
    # Datos de usuario para crear
    username   = serializers.CharField(write_only=True)
    password   = serializers.CharField(write_only=True)
    email      = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name  = serializers.CharField(write_only=True)

    # añadidos para Personal imagen 
    url_img    = serializers.URLField(write_only=True, required=False, allow_blank=True) 


    # Forma 1 (sencilla): por nombre del rol
    rol_nombre = serializers.ChoiceField(
        choices=[("PERSONAL","PERSONAL"), ("GUARDIA","GUARDIA")],
        write_only=True,
        required=False
    )
    # Forma 2 (alternativa): por id del rol, pero restringido a PERSONAL/GUARDIA
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.filter(nombre__in=["PERSONAL","GUARDIA"]),
        write_only=True,
        required=False
    )

    class Meta:
        model = Personal
        fields = [
            "username", "password", "email", "first_name", "last_name",
            "ocupacion", "horario_entrada", "horario_salida",
            "rol_nombre", "rol_id", "url_img"
        ]

    def validate(self, attrs):
        # Usuario duplicado
        if Usuario.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError({"username": "Ya existe un usuario con ese username"})

        # Debe venir rol_nombre o rol_id (uno de los dos). Si no viene, por defecto PERSONAL.
        rol_nombre = attrs.get("rol_nombre")
        rol_obj    = attrs.get("rol_id")
        if not rol_nombre and not rol_obj:
            attrs["rol_nombre"] = "PERSONAL"  # default

        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        # Extraer datos de usuario
        user_data = {
            "username":   validated_data.pop("username"),
            "email":      validated_data.pop("email"),
            "first_name": validated_data.pop("first_name"),
            "last_name":  validated_data.pop("last_name"),

            #extra
            "url_img":      validated_data.pop("url_img", ""), # Usa "" si no se envía
        }
        # Capturamos la contraseña de texto plano aquí
        raw_password = validated_data.pop("password") 

        # Resolver el rol a asignar
        rol_nombre = validated_data.pop("rol_nombre", None)
        rol_obj    = validated_data.pop("rol_id", None)

        if rol_obj is not None:
            rol_asignar = rol_obj
        else:
            rol_asignar, _ = Rol.objects.get_or_create(nombre=rol_nombre)

        # ------------------------------------------------------------------
        # 🟢 PASO CLAVE 1: Crear Usuario
        # ------------------------------------------------------------------
        usuario = Usuario.objects.create_user(**user_data)
        
        # 🟢 PASO CLAVE 2: Enviar el email con la contraseña de texto plano
        send_credentials_email(usuario.email, usuario.username, raw_password) 

        # 🟢 PASO CLAVE 3: Hashear y guardar la contraseña
        usuario.set_password(raw_password)
        usuario.save(update_fields=["password"])
        
        # ------------------------------------------------------------------
        # Asignar rol (PERSONAL o GUARDIA)
        RolUsuario.objects.get_or_create(usuario=usuario, rol=rol_asignar)

        # Crear Personal (perfil compartido para ambos roles)
        personal = Personal.objects.create(usuario=usuario, **validated_data)
        
        # ... (la lógica para la ocupación sigue igual) ...
        if not personal.ocupacion:
            if rol_asignar.nombre == "GUARDIA":
                personal.ocupacion = "GUARDIA"
            else:
                personal.ocupacion = "PERSONAL"
            personal.save(update_fields=["ocupacion"])

        return personal

# -----------------------------
# Personal - Read (Nuevo Serializador)
# -----------------------------
class PersonalReadSerializer(serializers.ModelSerializer):
    # 🟢 ANIDAMOS el serializador de usuario para traer todos sus datos
    usuario = UsuarioReadSerializer(read_only=True)
    
    # 🟢 Campo para mostrar el rol (asumiendo que el Personal siempre tiene un solo rol)
    rol_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Personal
        fields = [
            "id", 
            "ocupacion", 
            "horario_entrada", 
            "horario_salida",
            "usuario", # ¡Esto expone todos los campos del Usuario!
            "rol_nombre",
        ]
        
    def get_rol_nombre(self, obj):
        # Asume que un personal/guardia solo tiene un rol
        return obj.usuario.roles.first().nombre if obj.usuario.roles.exists() else "SIN ROL"

# -----------------------------
# Residente - Create
# Asigna rol PROPIETARIO o INQUILINO y vincula a una Unidad
# -----------------------------
class ResidenteUpsertSerializer(serializers.ModelSerializer):
    # Camino A: usar un usuario existente
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), write_only=True, required=False, source="usuario"
    )

    # Camino B: crear usuario nuevo (si NO mandas usuario_id)
    username   = serializers.CharField(write_only=True, required=False)
    password   = serializers.CharField(write_only=True, required=False)
    email      = serializers.EmailField(write_only=True, required=False, allow_blank=True)
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name  = serializers.CharField(write_only=True, required=False, allow_blank=True)
    ci         = serializers.CharField(write_only=True, required=False, allow_blank=True)
    telefono   = serializers.CharField(write_only=True, required=False, allow_blank=True)

    # Rol por id o por nombre (acepta PROPIETARIO/INQUILINO)
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.filter(nombre__in=["PROPIETARIO", "INQUILINO"]),
        write_only=True, required=False
    )
    rol_nombre = serializers.ChoiceField(
        choices=[("PROPIETARIO","PROPIETARIO"), ("INQUILINO","INQUILINO")],
        write_only=True, required=False
    )

    # Unidad requerida siempre
    unidad_id = serializers.PrimaryKeyRelatedField(
        queryset=UnidadHabitacional.objects.all(), write_only=True
    )

    class Meta:
        model = Residente
        fields = [
            "id",
            # Camino A
            "usuario_id",
            # Camino B
            "username", "password", "email", "first_name", "last_name", "ci", "telefono",
            # Rol
            "rol_id", "rol_nombre",
            # Unidad
            "unidad_id",

            "url_img", # 🌟 AÑADIR AQUÍ 🌟
        ]

    def validate(self, attrs):
        # Debe llegar usuario_id O (username + password) para crear
        tiene_usuario_existente = "usuario" in attrs  # por source="usuario"
        tiene_datos_nuevo = bool(attrs.get("username") and attrs.get("password"))

        if not (tiene_usuario_existente or tiene_datos_nuevo):
            raise serializers.ValidationError(
                "Debes enviar 'usuario_id' (usuario existente) o bien 'username' y 'password' para crear uno nuevo."
            )

        # Rol por id o por nombre (uno de los dos); si no viene, por defecto PROPIETARIO
        if not attrs.get("rol_id") and not attrs.get("rol_nombre"):
            attrs["rol_nombre"] = "PROPIETARIO"

        # Si vas a crear usuario nuevo, valida que no exista el username
        if not tiene_usuario_existente and Usuario.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError({"username": "Ya existe un usuario con ese username"})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        # Resolver usuario (existente o nuevo)
        usuario = validated_data.pop("usuario", None)  # viene si enviaron usuario_id
        if usuario is None:
            # Crear usuario nuevo con los campos enviados
            username   = validated_data.pop("username")
            password   = validated_data.pop("password")
            email      = validated_data.pop("email", "")
            first_name = validated_data.pop("first_name", "")
            last_name  = validated_data.pop("last_name", "")
            ci         = validated_data.pop("ci", "")
            telefono   = validated_data.pop("telefono", "")

            usuario = Usuario.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                ci=ci,
                telefono=telefono,
            )
            usuario.set_password(password)
            usuario.save(update_fields=["password"])
            
            # 🟢 PASO CLAVE para Residente: enviar email al crear
            send_credentials_email(usuario.email, usuario.username, password)

        # Resolver rol a asignar
        rol = validated_data.pop("rol_id", None)
        if rol is None:
            rol_nombre = validated_data.pop("rol_nombre")
            rol, _ = Rol.objects.get_or_create(nombre=rol_nombre)  # asegura PROPIETARIO/INQUILINO

        # Asegurar perfil Residente + asignar rol
        residente, _ = Residente.objects.get_or_create(usuario=usuario)
        RolUsuario.objects.get_or_create(usuario=usuario, rol=rol)

        # Vincular a unidad
        unidad = validated_data.pop("unidad_id")
        es_propietario = (rol.nombre == "PROPIETARIO")
        ResidenteUnidad.objects.get_or_create(
            residente=residente,
            unidad=unidad,
            defaults={"es_propietario": es_propietario}
        )
        
        # Actualizar la url_img si viene en los datos
        url_img = validated_data.pop("url_img", None)
        if url_img:
            usuario.url_img = url_img
            usuario.save(update_fields=["url_img"])

        return residente
