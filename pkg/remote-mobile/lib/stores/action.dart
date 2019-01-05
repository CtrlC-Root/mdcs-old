import 'package:remote/stores/model_notifier.dart';
import 'package:remote/stores/model_store.dart';
import 'package:remote/models/action.dart';

class ActionNotifier extends ModelNotifier<Action> {
  ActionNotifier(Action initialValue) : super(initialValue);
}

class ActionStore extends ModelStore<Action, ActionNotifier> {
  @override
  ActionNotifier createModelNotifier(Action value) {
    return ActionNotifier(value);
  }
}
