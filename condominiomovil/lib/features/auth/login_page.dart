import 'package:flutter/material.dart';

// ⬇️ Ajusta estos imports a tu estructura real de carpetas
import '../guardia/dashboard_guardia.dart';
import '../residentes/dashboard_residente.dart';
import '../mantenimiento/dashboard_personal.dart';
 
class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final emailCtrl = TextEditingController();
  final passCtrl  = TextEditingController();
  bool _obscure = true;

  // credenciales estáticas (mock)
  final _creds = <String, _Destino>{
    'residente@demo.com': _Destino(pass: '123456', builder: (_) => const DashboardResidente()),
    'guardia@demo.com'  : _Destino(pass: '123456', builder: (_) => const DashboardGuardia()),
    'personal@demo.com' : _Destino(pass: '123456', builder: (_) => const DashboardPersonal()),
   };

  void _login() {
    final email = emailCtrl.text.trim().toLowerCase();
    final pass  = passCtrl.text;

    final destino = _creds[email];
    if (destino != null && destino.pass == pass) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: destino.builder),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Credenciales inválidas')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;

    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Logo (placeholder)
                Container(
                  width: 96, height: 96,
                  decoration: BoxDecoration(
                    color: cs.primaryContainer,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Icon(Icons.apartment, size: 48, color: cs.onPrimaryContainer),
                ),
                const SizedBox(height: 24),
                const Text(
                  'INICIAR SESIÓN',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 24),

                TextField(
                  controller: emailCtrl,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(
                    labelText: 'Correo electrónico',
                    prefixIcon: Icon(Icons.email_outlined),
                  ),
                  onSubmitted: (_) => _login(),
                ),
                const SizedBox(height: 12),

                TextField(
                  controller: passCtrl,
                  obscureText: _obscure,
                  decoration: InputDecoration(
                    labelText: 'Contraseña',
                    prefixIcon: const Icon(Icons.lock_outline),
                    suffixIcon: IconButton(
                      icon: Icon(_obscure ? Icons.visibility_off : Icons.visibility),
                      onPressed: () => setState(() => _obscure = !_obscure),
                      tooltip: _obscure ? 'Mostrar' : 'Ocultar',
                    ),
                  ),
                  onSubmitted: (_) => _login(),
                ),

                const SizedBox(height: 12),
                Align(
                  alignment: Alignment.centerLeft,
                  child: TextButton(
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Recuperación deshabilitada en modo demo')),
                      );
                    },
                    child: const Text('¿Olvidaste tu contraseña?'),
                  ),
                ),

                const SizedBox(height: 8),
                ElevatedButton(
                  onPressed: _login,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text('Iniciar Sesión'),
                ),

                const SizedBox(height: 16),
                const Divider(),
                const SizedBox(height: 8),
                // Ayuda para pruebas: muestra usuarios demo
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: const [
                        Text('Usuarios demo (correo / 123456):',
                            style: TextStyle(fontWeight: FontWeight.w600)),
                        SizedBox(height: 6),
                        Text('• residente@demo.com'),
                        Text('• guardia@demo.com'),
                        Text('• personal@demo.com'),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _Destino {
  final String pass;
  final WidgetBuilder builder;
  const _Destino({required this.pass, required this.builder});
}
