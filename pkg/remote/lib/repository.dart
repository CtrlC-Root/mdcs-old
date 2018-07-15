import 'package:remote/models/models.dart';
import 'package:remote/stores/stores.dart';

class Repository {
  final ActionStore actions = ActionStore();
  final TaskStore tasks = TaskStore();

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
