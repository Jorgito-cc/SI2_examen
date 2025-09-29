import 'package:flutter/material.dart';

class ReservasPage extends StatefulWidget {
  const ReservasPage({super.key});
  @override
  State<ReservasPage> createState() => _ReservasPageState();
}

class _ReservasPageState extends State<ReservasPage> {
  DateTime _fecha = DateTime.now();
  String? _area; String? _hora;
  final _areas = const ['Piscina', 'Salón de eventos', 'Cancha', 'Gimnasio'];
  final _horarios = const ['08:00-09:00','09:00-10:00','10:00-11:00','18:00-19:00','19:00-20:00'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Reservas')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('Selecciona fecha', style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          CalendarDatePicker(
            initialDate: _fecha, firstDate: DateTime.now().subtract(const Duration(days: 1)),
            lastDate: DateTime.now().add(const Duration(days: 90)),
            onDateChanged: (d) => setState(() => _fecha = d),
          ),
          const SizedBox(height: 8),
          DropdownButtonFormField<String>(
            value: _area, items: _areas.map((a)=> DropdownMenuItem(value:a, child: Text(a))).toList(),
            decoration: const InputDecoration(labelText: 'Área común'),
            onChanged: (v)=> setState(()=> _area = v),
          ),
          const SizedBox(height: 8),
          DropdownButtonFormField<String>(
            value: _hora, items: _horarios.map((h)=> DropdownMenuItem(value:h, child: Text(h))).toList(),
            decoration: const InputDecoration(labelText: 'Horario'),
            onChanged: (v)=> setState(()=> _hora = v),
          ),
          const SizedBox(height: 12),
          FilledButton.icon(
            onPressed: (_area!=null && _hora!=null) ? _confirmar : null,
            icon: const Icon(Icons.event_available),
            label: const Text('Confirmar reserva'),
          ),
          const SizedBox(height: 20),
          Text('Reservas recientes', style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          ...[
            'Piscina • 21/10 • 18:00-19:00 • Confirmada',
            'Salón • 15/10 • 10:00-11:00 • Confirmada',
          ].map((s)=> Card(child: ListTile(leading: const Icon(Icons.event_available_outlined), title: Text(s)))),
        ],
      ),
    );
  }

  void _confirmar() {
    final f = '${_fecha.day}/${_fecha.month}/${_fecha.year}';
    showDialog(context: context, builder: (_) {
      return AlertDialog(
        title: const Text('Reserva creada'),
        content: Text('Área: $_area\nFecha: $f\nHorario: $_hora\nCódigo: RSV-${DateTime.now().millisecondsSinceEpoch}'),
        actions: [ TextButton(onPressed: ()=> Navigator.pop(context), child: const Text('OK')) ],
      );
    });
  }
}
