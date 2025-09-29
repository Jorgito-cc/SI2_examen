import 'package:flutter/material.dart';

class PerfilPage extends StatelessWidget {
  const PerfilPage({super.key});

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Scaffold(
      appBar: AppBar(title: const Text('Perfil')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Center(
            child: CircleAvatar(
              radius: 48,
              backgroundColor: cs.primaryContainer,
              child: const Icon(Icons.person, size: 48),
            ),
          ),
          const SizedBox(height: 12),
          Center(
            child: Text('Carlos Méndez', style: Theme.of(context).textTheme.titleLarge),
          ),
          Center(child: Text('Técnico de Mantenimiento')),
          const SizedBox(height: 16),
          const ListTile(
            leading: Icon(Icons.badge_outlined),
            title: Text('Legajo'),
            subtitle: Text('PM-00123'),
          ),
          const ListTile(
            leading: Icon(Icons.phone_outlined),
            title: Text('Teléfono'),
            subtitle: Text('+591 700-00000'),
          ),
          const ListTile(
            leading: Icon(Icons.email_outlined),
            title: Text('Correo'),
            subtitle: Text('personal@demo.com'),
          ),
          const SizedBox(height: 12),
          FilledButton.icon(
            onPressed: () {
              Navigator.of(context).pop(); // en demo: vuelve al login
            },
            icon: const Icon(Icons.logout),
            label: const Text('Cerrar sesión'),
          )
        ],
      ),
    );
  }
}
