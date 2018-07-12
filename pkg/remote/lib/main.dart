import 'package:flutter/material.dart';
import 'package:remote/screens/screens.dart';

void main() => runApp(RemoteApp());

class RemoteApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Remote Control',
      initialRoute: '/',
      routes: {
        '/': (context) => DashboardScreen()
      },
    );
  }
}
