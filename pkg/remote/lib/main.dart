import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/jobs/jobs.dart';
import 'package:remote/screens/screens.dart';

void main() {
  final JobQueue queue = JobQueue();
  queue.start().then((dynamic ignore) {
    runApp(RemoteApp(queue: queue));
  });
  //runApp(RemoteApp(queue: queue));
}

class RemoteApp extends StatelessWidget {
  final JobQueue queue;
  final Repository repository = Repository();

  RemoteApp({Key key, @required JobQueue queue}) : this.queue = queue, super(key: key) {
    // TODO: replace this debugging code
    this.queue.run<InitialFetchJob>(InitialFetchJob(Uri(scheme: 'http', host: 'localhost', port: 5000)))
      .then((InitialFetchJob initialFetch) {
        this.repository.actions.values = initialFetch.actions;
        this.repository.tasks.values = initialFetch.tasks;
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
