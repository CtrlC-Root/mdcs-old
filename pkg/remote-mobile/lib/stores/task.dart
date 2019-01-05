import 'package:remote/stores/model_notifier.dart';
import 'package:remote/stores/model_store.dart';
import 'package:remote/models/task.dart';

class TaskNotifier extends ModelNotifier<Task> {
  TaskNotifier(Task initialValue) : super(initialValue);
}

class TaskStore extends ModelStore<Task, TaskNotifier> {
  @override
  TaskNotifier createModelNotifier(Task value) {
    return TaskNotifier(value);
  }
}
