import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/jobs/jobs.dart';
import 'package:remote/screens/screens.dart';

/// Application entry point.
void main() {
  runApp(RemoteApp());
}

/// Remote control application top-level widget.
class RemoteApp extends StatelessWidget {
  final JobQueue queue = JobQueue();
  final Repository repository = Repository();

  RemoteApp({Key key}) : super(key: key) {
    // start the job queue and initialize the repository
    this.queue.start()
      .then((JobQueue queue) {
        return queue.run(InitialFetchJob(Uri(scheme: 'http', host: 'localhost', port: 5000)));
      })
      .then((InitialFetchJob initialFetch) {
        this.repository.actions.values = initialFetch.actions;
        this.repository.tasks.values = initialFetch.tasks;
      })
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
        '/': (context) => DashboardScreen(queue: queue, repository: repository)
      },
    );
  }
}
