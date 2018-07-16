import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/jobs/jobs.dart';
import 'package:remote/screens/screens.dart';

/// Application entry point.
void main() {
  final JobQueue queue = JobQueue();
  final Repository repository = Repository(queue, Uri(scheme: 'http', host: 'localhost', port: 5000));

  queue.start().then((JobQueue ignore) {
    runApp(RemoteApp(repository: repository));
  });
}

/// Remote control application top-level widget.
class RemoteApp extends StatelessWidget {
  final Repository repository;

  RemoteApp({Key key, @required this.repository}) : super(key: key) {
    // initialize repository
    this.repository.fetchAll()
      .catchError((e) {
        debugPrint("UH OH: ${e.toString()}");
      });
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
