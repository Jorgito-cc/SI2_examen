import 'package:flutter/material.dart';
import 'tarea_detalle_page.dart';

class TareasPage extends StatefulWidget {
  const TareasPage({super.key});
  @override
  State<TareasPage> createState() => _TareasPageState();
}

class _TareasPageState extends State<TareasPage> {
  final List<_Tarea> _items = [
    _Tarea('Reparar luminaria', 'Bloque B – Piso 2', 'ALTA',
        estado: 'PENDIENTE', asignada: DateTime.now().subtract(const Duration(hours: 2))),
    _Tarea('Fuga de agua', 'Torre A – Dpto 803', 'ALTA',
        estado: 'EN PROCESO', asignada: DateTime.now().subtract(const Duration(hours: 1))),
    _Tarea('Pintura baranda', 'Piscina', 'MEDIA',
        estado: 'COMPLETADA', asignada: DateTime.now().subtract(const Duration(days: 1))),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Tareas asignadas')),
      body: ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: _items.length,
        separatorBuilder: (_, __) => const SizedBox(height: 8),
        itemBuilder: (_, i) {
          final t = _items[i];
          final chipColor = switch (t.estado) {
            'PENDIENTE' => Colors.orange,
            'EN PROCESO' => Colors.blue,
            _ => Colors.green,
          };
          return Card(
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: chipColor.withOpacity(.15),
                child: Icon(Icons.build, color: chipColor),
              ),
              title: Text(t.titulo),
              subtitle: Text('${t.ubicacion} • Prioridad ${t.prioridad}'),
              trailing: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Chip(
                    label: Text(t.estado),
                    visualDensity: VisualDensity.compact,
                  ),
                  Text(_fmt(t.asignada), style: Theme.of(context).textTheme.bodySmall),
                ],
              ),
              onTap: () async {
                final updated = await Navigator.push<_Tarea>(
                  context,
                  MaterialPageRoute(builder: (_) => TareaDetallePage(tarea: t)),
                );
                if (updated != null) setState(() => _items[i] = updated);
              },
            ),
          );
        },
      ),
    );
  }

  String _fmt(DateTime dt) =>
      '${dt.day}/${dt.month} ${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}';
}

class _Tarea {
  String titulo, ubicacion, prioridad, estado;
  DateTime asignada;
  String? descripcion;
  _Tarea(this.titulo, this.ubicacion, this.prioridad,
      {required this.estado, required this.asignada, this.descripcion});
}
