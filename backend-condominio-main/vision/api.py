""" from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import FaceEnrollSerializer, FaceRecognizeSerializer
from .services.face_service import enroll_face, recognize_face

class FaceEnrollAPI(APIView):
    permission_classes = [permissions.IsAdminUser]  # o la que uses

    def post(self, request):
        s = FaceEnrollSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        result = enroll_face(
            usuario_id=s.validated_data["usuario_id"],
            data_urls=s.validated_data["imagenes"],
            label=s.validated_data.get("label", "principal"),
        )
        return Response(result, status=status.HTTP_201_CREATED)

class FaceRecognizeAPI(APIView):
    permission_classes = [permissions.AllowAny]  # ajusta según tu flujo

    def post(self, request):
        s = FaceRecognizeSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        result = recognize_face(
            data_url=s.validated_data["imagen"],
            umbral=s.validated_data.get("umbral"),
        )
        return Response(result, status=status.HTTP_200_OK)
 """