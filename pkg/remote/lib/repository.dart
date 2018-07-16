import 'dart:async';
import 'package:remote/models/models.dart';
import 'package:remote/stores/stores.dart';
import 'package:remote/jobs/jobs.dart';

class Repository {
  final JobQueue _queue;
  final Uri reactorUri;
  final ActionStore actions = ActionStore();
  final TaskStore tasks = TaskStore();

  Repository(JobQueue queue, Uri reactorUri) : this._queue = queue, this.reactorUri = reactorUri;

  Future fetchAll() {
    return this._queue.run(InitialFetchJob(this.reactorUri))
      .then((InitialFetchJob initialFetch) {
        this.actions.values = initialFetch.actions;
        this.tasks.values = initialFetch.tasks;
      });
  }

  Future createTask(Action action) {
    return this._queue.run(CreateTaskJob(this.reactorUri, action))
      .then((CreateTaskJob createTask) {
        this.tasks.add(createTask.task);
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

  void loadTestData() {
    final actionOne = Action(
      uuid: "one",
      title: "More Light",
      description: "Make everything brighter",
      content: "more_light()",
    );

    final actionTwo = Action(
      uuid: "two",
      title: "Less Light",
      description: "Make everything darker",
      content: "less_light()",
    );

    this.actions.values = [actionOne, actionTwo];
    this.tasks.values = [
      Task(
        uuid: "one",
        actionUuid: actionOne.uuid,
        state: TaskState.running,
        created: DateTime.now(),
        modified: DateTime.now(),
        output: "",
      ),
      Task(
        uuid: "two",
        actionUuid: actionTwo.uuid,
        state: TaskState.running,
        created: DateTime.now(),
        modified: DateTime.now(),
        output: "",
      ),
    ];
  }
}
