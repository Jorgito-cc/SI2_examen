import 'package:flutter/material.dart';
import 'visitante_form.dart';

class VisitantesPage extends StatefulWidget {
  const VisitantesPage({super.key});
  @override State<VisitantesPage> createState() => _VisitantesPageState();
}

class _VisitantesPageState extends State<VisitantesPage> {
  final _q = TextEditingController();
  final List<_Visitante> _data = [
    _Visitante('Juan Pérez', 'CI 543219', 'Torre A • Dpto 12', ingreso: DateTime.now().subtract(const Duration(minutes: 18))),
    _Visitante('María López', 'CI 658741', 'Bloque B • Casa 3', ingreso: DateTime.now().subtract(const Duration(hours: 1, minutes: 7))),
    _Visitante('Carlos Ruiz', 'CI 987654', 'Torre C • Dpto 8', ingreso: DateTime.now().subtract(const Duration(hours: 3))),
  ];

  @override
  Widget build(BuildContext context) {
    final filtered = _q.text.isEmpty ? _data : _data.where((v) =>
      v.nombre.toLowerCase().contains(_q.text.toLowerCase()) || v.doc.contains(_q.text)).toList();

    return Scaffold(
      appBar: AppBar(title: const Text('Control de Visitantes')),
      body: Column(children: [
        Padding(
          padding: const EdgeInsets.all(16),
          child: TextField(
            controller: _q,
            decoration: InputDecoration(
              prefixIcon: const Icon(Icons.search),
              hintText: 'Buscar por nombre o documento',
              suffixIcon: _q.text.isEmpty ? null : IconButton(
                icon: const Icon(Icons.clear),
                onPressed: () { _q.clear(); setState((){}); },
              ),
            ),
            onChanged: (_) => setState((){}),
          ),
        ),
        Expanded(
          child: ListView.separated(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            itemCount: filtered.length,
            separatorBuilder: (_, __) => const SizedBox(height: 8),
            itemBuilder: (_, i) {
              final v = filtered[i];
              return Card(
                child: ListTile(
                  leading: const CircleAvatar(child: Icon(Icons.person)),
                  title: Text(v.nombre),
                  subtitle: Text('${v.doc} • ${v.unidad}\nIngreso: ${_fmt(v.ingreso)}${v.salida!=null ? '\nSalida: ${_fmt(v.salida!)}' : ''}'),
                  isThreeLine: true,
                  trailing: v.salida == null
                      ? ElevatedButton.icon(
                          icon: const Icon(Icons.logout, size: 16),
                          label: const Text('Registrar salida'),
                          onPressed: () { setState(()=> v.salida = DateTime.now()); },
                        )
                      : const Chip(label: Text('Finalizado')),
                ),
              );
            },
          ),
        ),
      ]),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          await Navigator.push(context, MaterialPageRoute(builder: (_) => const VisitanteFormPage()));
        },
        icon: const Icon(Icons.person_add_alt_1),
        label: const Text('Nuevo ingreso'),
      ),
    );
  }

  String _fmt(DateTime dt) {
    final h = dt.hour.toString().padLeft(2,'0');
    final m = dt.minute.toString().padLeft(2,'0');
    return '${dt.day}/${dt.month} $h:$m';
  }
}

class _Visitante {
  final String nombre; final String doc; final String unidad;
  final DateTime ingreso; DateTime? salida;
  _Visitante(this.nombre, this.doc, this.unidad, {required this.ingreso});
}
