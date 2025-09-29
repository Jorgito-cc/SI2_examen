import 'package:flutter/material.dart';

class AlertasPage extends StatefulWidget {
  const AlertasPage({super.key});
  @override State<AlertasPage> createState() => _AlertasPageState();
}

class _AlertasPageState extends State<AlertasPage> {
  final List<_Alerta> _items = [
    _Alerta('Persona no autorizada en zona restringida', 'Acceso Principal', DateTime.now(), 'NUEVA'),
    _Alerta('Vehículo mal estacionado', 'Parqueo Norte', DateTime.now().subtract(const Duration(minutes: 8)), 'NUEVA'),
    _Alerta('Perro suelto detectado', 'Patio B', DateTime.now().subtract(const Duration(hours: 1, minutes: 20)), 'NUEVA'),
  ];

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Scaffold(
      appBar: AppBar(title: const Text('Alertas en tiempo real')),
      body: ListView.separated(
        padding: const EdgeInsets.all(16),
        separatorBuilder: (_, __) => const SizedBox(height: 8),
        itemCount: _items.length,
        itemBuilder: (_, i) {
          final a = _items[i];
          return Card(
            child: ListTile(
              leading: Icon(Icons.warning_amber_rounded, color: cs.primary),
              title: Text(a.titulo),
              subtitle: Text('${a.ubicacion} • ${_fmt(a.fecha)} • ${a.estado}'),
              trailing: Wrap(spacing: 8, children: [
                OutlinedButton(onPressed: () => setState(() => a.estado = 'DESCARTADA'), child: const Text('Descartar')),
                ElevatedButton(onPressed: () => setState(() => a.estado = 'CONFIRMADA'), child: const Text('Confirmar')),
              ]),
              onTap: () => _detalle(context, a),
            ),
          );
        },
      ),
    );
  }

  void _detalle(BuildContext context, _Alerta a) {
    showDialog(context: context, builder: (_) {
      return AlertDialog(
        title: Text(a.titulo),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(height: 160, color: Colors.black12, child: const Center(child: Icon(Icons.image, size: 48))),
            const SizedBox(height: 12),
            Text('Ubicación: ${a.ubicacion}\nHora: ${_fmt(a.fecha)}\nEstado: ${a.estado}'),
          ],
        ),
        actions: [ TextButton(onPressed: ()=> Navigator.pop(context), child: const Text('Cerrar')) ],
      );
    });
  }

  String _fmt(DateTime dt) {
    final h = dt.hour.toString().padLeft(2,'0');
    final m = dt.minute.toString().padLeft(2,'0');
    return '${dt.day}/${dt.month} $h:$m';
  }
}

class _Alerta { final String titulo; final String ubicacion; final DateTime fecha; String estado; _Alerta(this.titulo, this.ubicacion, this.fecha, this.estado); }
