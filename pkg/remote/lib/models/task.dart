import 'package:remote/models/model.dart';

/// The state of a task.
enum TaskState {
  pending,
  running,
  cancelled,
  completed,
  failed
}

/// A task to run an action.
class Task extends Model {
  String uuid;
  String actionUuid;
  TaskState state;
  DateTime created;
  DateTime modified;
  String output;

  Task({this.uuid, this.actionUuid, this.state, this.created, this.modified, this.output});

  Task.fromJSON(Map<String, dynamic> data) {
    this.uuid = data['uuid'] as String;
    this.actionUuid = data['action_uuid'] as String;
    this.created = DateTime.parse(data['created'] as String);
    this.modified = DateTime.parse(data['modified'] as String);
    this.output = data['output'] as String;

    switch (data['state']) {
      case 'pending':
        this.state = TaskState.pending;
        break;

      case 'running':
        this.state = TaskState.running;
        break;

      case 'cancelled':
        this.state = TaskState.cancelled;
        break;

      case 'completed':
        this.state = TaskState.completed;
        break;

      case 'failed':
        this.state = TaskState.failed;
        break;
    }
  }

  @override
  String get primaryKey => this.uuid;
}
