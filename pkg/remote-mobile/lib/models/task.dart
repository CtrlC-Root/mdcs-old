import 'package:remote/models/model.dart';
import 'package:remote/models/control.dart';
import 'package:remote/models/button_control.dart';
import 'package:remote/models/color_control.dart';

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
  final String controlSetUuid;
  final TaskState state;
  final DateTime created;
  final DateTime modified;
  final Map<String, ControlValue> input;

  Task({this.uuid, this.controlSetUuid, this.state, this.created, this.modified, this.input});
  Task.fromJSON(Map<String, dynamic> data) :
    this.uuid = data['uuid'] as String,
    this.controlSetUuid = data['controlset_uuid'] as String,
    this.state = Task.parseState(data['state'] as String),
    this.created = DateTime.parse(data['created'] as String),
    this.modified = DateTime.parse(data['modified'] as String),
    this.input = Task.parseInputValues(data['input']);

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

  static Map<String, ControlValue> parseInputValues(Map<String, dynamic> data) {
    return data.map((String name, dynamic value) {
      return MapEntry(name, Task.parseControlValue(value));
    });
  }

  static ControlValue parseControlValue(Map<String, dynamic> data) {
    final type = Control.parseControlType(data['type'] as String);
    switch (type) {
      case ControlType.button:
        return ButtonValue.fromJSON(data);

      case ControlType.color:
        return ColorValue.fromJSON(data);

      case ControlType.none:
        // XXX: this shouldn't happen, what do we do here?
        return ControlValue();
    }

    // XXX: why does the compiler think this is necessary?
    return ControlValue();
  }

  @override
  String get primaryKey => this.uuid;
}
