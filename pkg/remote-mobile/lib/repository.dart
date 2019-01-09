import 'dart:async';
import 'package:remote/models/models.dart';
import 'package:remote/stores/stores.dart';
import 'package:remote/jobs/jobs.dart';

class Repository {
  final JobQueue _queue;
  final Uri reactorUri;

  final ControlSetStore controlSets = ControlSetStore();
  final ControlStore controls = ControlStore();
  final TaskStore tasks = TaskStore();

  Repository(JobQueue queue, Uri reactorUri) : this._queue = queue, this.reactorUri = reactorUri;

  Future fetchAll() {
    return this._queue.run(FetchAllJob(this.reactorUri))
      .then((FetchAllJob initialFetch) {
        this.controlSets.values = initialFetch.controlSets;
        this.controls.values = initialFetch.controls;
        this.tasks.values = initialFetch.tasks;
      });
  }

  Future<List<Task>> fetchPendingTasks() {
    final Set<TaskState> pendingStates = Set.of([TaskState.pending, TaskState.running]);
    final refreshJobs = this.tasks.values
      .where((Task task) => pendingStates.contains(task.state))
      .map((Task task) => this._queue.run(FetchTaskJob(this.reactorUri, task.primaryKey)));

    return Future.wait(refreshJobs)
      .then((List<FetchTaskJob> jobs) => jobs.map((FetchTaskJob job) => job.task).toList())
      .then((List<Task> tasks) {
        for (Task task in tasks) {
          this.tasks.getNotifierByKey(task.primaryKey).value = task;
        }

        return tasks;
      });
  }
}
