import 'package:flutter/foundation.dart';
import 'package:remote/models/model.dart';
import 'package:remote/stores/model_notifier.dart';

/// Abstract base class for model stores.
abstract class ModelStore<T extends Model, N extends ModelNotifier<T>> extends ChangeNotifier {
  Map<int, N> _values;

  ModelStore(List<T> initialValues) {
    this._values = Map.fromIterable(
      initialValues,
      key: (value) => value.hashCode,
      value: (value) => this.createModelNotifier(value)
    );
  }

  /// Create an instance of the concrete model notifier from the given concrete model instance.
  /// See https://github.com/dart-lang/sdk/issues/10667 for why this can't be done in the constructor above.
  @protected
  N createModelNotifier(T value);

  List<T> get values {
    return this._values.values.map((N notifier) => notifier.value).toList();
  }

  List<N> get notifiers {
    return this._values.values.toList();
  }

  set values(List<T> newValues) {
    // TODO compare the two lists and only create/remove notifiers as necessary
    // XXX should we set notifier values to null when removing them?

    this._values = Map.fromIterable(
      newValues,
      key: (value) => value.hashCode,
      value: (value) => this.createModelNotifier(value)
    );
  }

  void add(T value) {
    this._values[value.hashCode] = this.createModelNotifier(value);
    this.notifyListeners();
  }

  void remove(T value) {
    // XXX should we set the notifier value to null before removing it?
    // XXX this._values[value.hashCode].value = null

    this._values.remove(value.hashCode);
    this.notifyListeners();
  }

  N getNotifierFor(T value) {
    // TODO: this._modelNotifiers.containsKey(value.hashCode)
    return this._values[value.hashCode];
  }
}
