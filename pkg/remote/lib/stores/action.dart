import 'package:remote/stores/model_notifier.dart';
import 'package:remote/stores/model_store.dart';
import 'package:remote/models/action.dart';

class ActionNotifier extends ModelNotifier<Action> {
  ActionNotifier(Action initialValue) : super(initialValue);

  void update({String uuid, String title, String description, String content}) {
    this.value = Action(
      uuid: uuid ?? this.value.uuid,
      title: title ?? this.value.title,
      description: description ?? this.value.description,
      content: content ?? this.value.content
    );
  }
}

class ActionStore extends ModelStore<Action, ActionNotifier> {
  ActionStore() : super([]);

  @override
  ActionNotifier createModelNotifier(Action value) {
    return ActionNotifier(value);
  }
}
