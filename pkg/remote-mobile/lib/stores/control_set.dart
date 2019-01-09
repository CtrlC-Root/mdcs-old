import 'package:remote/stores/model_notifier.dart';
import 'package:remote/stores/model_store.dart';
import 'package:remote/models/control_set.dart';

class ControlSetNotifier extends ModelNotifier<ControlSet> {
  ControlSetNotifier(ControlSet initialValue) : super(initialValue);
}

class ControlSetStore extends ModelStore<ControlSet, ControlSetNotifier> {
  @override
  ControlSetNotifier createModelNotifier(ControlSet value) {
    return ControlSetNotifier(value);
  }
}
