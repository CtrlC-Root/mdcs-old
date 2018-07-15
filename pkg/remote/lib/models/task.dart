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
  final String uuid;
  final String actionUuid;
  final TaskState state;
  final DateTime created;
  final DateTime modified;
  final String output;

  Task({this.uuid, this.actionUuid, this.state, this.created, this.modified, this.output});

  Task.fromJSON(Map<String, dynamic> data) :
    this.uuid = data['uuid'] as String,
    this.actionUuid = data['action_uuid'] as String,
    this.state = Task.parseState(data['state'] as String),
    this.created = DateTime.parse(data['created'] as String),
    this.modified = DateTime.parse(data['modified'] as String),
    this.output = data['output'] as String;

  static TaskState parseState(String value) {
    switch (value.toLowerCase()) {
      case 'pending': return TaskState.pending;
      case 'running': return TaskState.running;
      case 'cancelled': return TaskState.cancelled;
      case 'completed': return TaskState.completed;
      case 'failed': return TaskState.failed;
      default: throw Exception('unknown task state: $value');
    }
  }

  @override
  String get primaryKey => this.uuid;
}
