import 'package:flutter/material.dart';

class FinanzasPage extends StatefulWidget {
  const FinanzasPage({super.key});
  @override
  State<FinanzasPage> createState() => _FinanzasPageState();
}

class _FinanzasPageState extends State<FinanzasPage> {
  final List<_Cuota> _cuotas = [
    _Cuota('Sep 2025', 320, DateTime(2025, 9, 30), 'PENDIENTE'),
    _Cuota('Ago 2025', 320, DateTime(2025, 8, 31), 'PAGADA', recibo: 'REC-00021'),
    _Cuota('Jul 2025', 320, DateTime(2025, 7, 31), 'PAGADA', recibo: 'REC-00020'),
  ];

  @override
  Widget build(BuildContext context) {
    final pendientes = _cuotas.where((c) => c.estado == 'PENDIENTE').toList();
    final pagadas = _cuotas.where((c) => c.estado == 'PAGADA').toList();

    return Scaffold(
      appBar: AppBar(title: const Text('Finanzas')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (pendientes.isNotEmpty)
            ...pendientes.map((c) => _CuotaCard(
              cuota: c,
              action: FilledButton.icon(
                onPressed: () => _pagar(c),
                icon: const Icon(Icons.payment),
                label: const Text('Pagar ahora'),
              ),
            )),
          const SizedBox(height: 12),
          Text('Historial de pagos', style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          ...pagadas.map((c) => _CuotaCard(
            cuota: c,
            action: OutlinedButton.icon(
              onPressed: () => _verRecibo(c),
              icon: const Icon(Icons.receipt_long),
              label: const Text('Comprobante'),
            ),
          )),
        ],
      ),
    );
  }

  void _pagar(_Cuota c) async {
    // MOCK: confirmación de pago
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Confirmar pago'),
        content: Text('Vas a pagar Bs. ${c.monto} (${c.periodo}).'),
        actions: [
          TextButton(onPressed: ()=> Navigator.pop(context, false), child: const Text('Cancelar')),
          FilledButton(onPressed: ()=> Navigator.pop(context, true), child: const Text('Pagar')),
        ],
      ),
    );
    if (ok == true) {
      setState(() {
        c.estado = 'PAGADA';
        c.recibo = 'REC-${DateTime.now().millisecondsSinceEpoch}';
      });
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Pago realizado (mock)')));
    }
  }

  void _verRecibo(_Cuota c) {
    showDialog(context: context, builder: (_) {
      return AlertDialog(
        title: const Text('Comprobante'),
        content: Text('Recibo: ${c.recibo}\nPeriodo: ${c.periodo}\nMonto: Bs. ${c.monto}'),
        actions: [ TextButton(onPressed: ()=> Navigator.pop(context), child: const Text('Cerrar')) ],
      );
    });
  }
}

class _CuotaCard extends StatelessWidget {
  final _Cuota cuota;
  final Widget action;
  const _CuotaCard({required this.cuota, required this.action});
  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    final venc = '${cuota.vencimiento.day}/${cuota.vencimiento.month}/${cuota.vencimiento.year}';
    final chipColor = cuota.estado == 'PENDIENTE' ? cs.errorContainer : cs.primaryContainer;
    final chipText = cuota.estado == 'PENDIENTE' ? cs.onErrorContainer : cs.onPrimaryContainer;

    return Card(
      child: ListTile(
        leading: CircleAvatar(backgroundColor: chipColor, child: Text(cuota.periodo.substring(0,3))),
        title: Text('Cuota ${cuota.periodo} • Bs. ${cuota.monto}'),
        subtitle: Text('Vence: $venc'),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Chip(label: Text(cuota.estado), backgroundColor: chipColor, labelStyle: TextStyle(color: chipText)),
            const SizedBox(height: 4),
            action,
          ],
        ),
        isThreeLine: true,
      ),
    );
  }
}

class _Cuota {
  final String periodo; final double monto; final DateTime vencimiento;
  String estado; String? recibo;
  _Cuota(this.periodo, this.monto, this.vencimiento, this.estado, {this.recibo});
}
