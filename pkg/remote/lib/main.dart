import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/screens/screens.dart';

void main() => runApp(RemoteApp());

class RemoteApp extends StatelessWidget {
  final Repository repository = Repository();

  RemoteApp({Key key}) : super(key: key) {
    // TODO: replace this debugging code
    this.repository.loadTestData();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Remote Control',
      initialRoute: '/',
      routes: {
        '/': (context) => DashboardScreen(repository: repository)
      },
    );
  }
}
