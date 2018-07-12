import 'package:remote/models/model.dart';
import 'package:remote/models/action.dart';

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
    Action action;
    TaskState state;
    DateTime created;
    DateTime modified;
    String output;
}
