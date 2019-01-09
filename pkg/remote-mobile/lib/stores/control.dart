import 'package:remote/stores/model_notifier.dart';
import 'package:remote/stores/model_store.dart';
import 'package:remote/models/control.dart';

class ControlNotifier extends ModelNotifier<Control> {
  ControlNotifier(Control initialValue) : super(initialValue);
}

class ControlStore extends ModelStore<Control, ControlNotifier> {
  @override
  ControlNotifier createModelNotifier(Control value) {
    return ControlNotifier(value);
  }
}
