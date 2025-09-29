import 'package:flutter/material.dart';

class NotificacionesPage extends StatefulWidget {
  const NotificacionesPage({super.key});
  @override
  State<NotificacionesPage> createState() => _NotificacionesPageState();
}

class _NotificacionesPageState extends State<NotificacionesPage> {
  final List<_Notif> _items = [
    _Notif('Vencimiento de cuota', 'Tu cuota vence el 30/10', DateTime.now(), leida: false, tipo: 'finanza'),
    _Notif('Portón bloqueado', 'Se bloqueó temporalmente por mantenimiento', DateTime.now().subtract(const Duration(hours: 2)), tipo: 'seguridad'),
    _Notif('Reserva próxima', 'Piscina hoy 18:00', DateTime.now().subtract(const Duration(days: 1)), tipo: 'reserva'),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Notificaciones')),
      body: ListView.separated(
        padding: const EdgeInsets.all(16),
        separatorBuilder: (_, __) => const SizedBox(height: 8),
        itemCount: _items.length,
        itemBuilder: (_, i) {
          final n = _items[i];
          final icon = switch (n.tipo) {
            'finanza' => Icons.account_balance_wallet_outlined,
            'seguridad' => Icons.shield_outlined,
            'reserva' => Icons.event_available_outlined,
            _ => Icons.notifications_outlined,
          };
          return Card(
            child: ListTile(
              leading: Icon(icon),
              title: Text(n.titulo),
              subtitle: Text(n.mensaje),
              trailing: Wrap(spacing: 8, children: [
                if (!n.leida) FilledButton(onPressed: () => setState(()=> n.leida = true), child: const Text('Marcar leído')),
                OutlinedButton(onPressed: () => _ver(n), child: const Text('Ver')),
              ]),
            ),
          );
        },
      ),
    );
  }

  void _ver(_Notif n) {
    setState(()=> n.leida = true);
    showDialog(context: context, builder: (_) {
      return AlertDialog(
        title: Text(n.titulo),
        content: Text('${n.mensaje}\n\n${_fmt(n.fecha)}'),
        actions: [ TextButton(onPressed: ()=> Navigator.pop(context), child: const Text('Cerrar')) ],
      );
    });
  }

  String _fmt(DateTime dt){
    final d = '${dt.day}/${dt.month}';
    final h = '${dt.hour.toString().padLeft(2,'0')}:${dt.minute.toString().padLeft(2,'0')}';
    return '$d $h';
  }
}

class _Notif {
  final String titulo, mensaje, tipo; final DateTime fecha; bool leida;
  _Notif(this.titulo, this.mensaje, this.fecha, {this.tipo='general', this.leida=true});
}
