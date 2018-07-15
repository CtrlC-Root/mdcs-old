import 'package:flutter/foundation.dart';
import 'package:remote/models/model.dart';
import 'package:remote/stores/model_notifier.dart';

/// Abstract base class for model stores.
abstract class ModelStore<T extends Model, N extends ModelNotifier<T>> extends ChangeNotifier {
  Map<String, N> _values;

  /// Default constructor.
  ModelStore() {
    this._values = Map<String, N>();
  }

  /// Create an instance of the concrete model notifier from the given concrete model instance.
  /// See https://github.com/dart-lang/sdk/issues/10667 for why this can't be done in the constructor above.
  @protected
  N createModelNotifier(T value);

  /// Get model notifiers.
  List<N> get notifiers {
    return this._values.values.toList();
  }

  /// Get model values.
  List<T> get values {
    return this._values.values.map((N notifier) => notifier.value).toList();
  }

  /// Set model values.
  set values(List<T> newValues) {
    // TODO compare the two lists and only create/remove notifiers as necessary
    // XXX should we set notifier values to null when removing them?

    this._values = Map.fromIterable(
      newValues,
      key: (value) => value.primaryKey,
      value: (value) => this.createModelNotifier(value)
    );

    this.notifyListeners();
  }

  /// Add a single model value.
  void add(T value) {
    this._values[value.primaryKey] = this.createModelNotifier(value);
    this.notifyListeners();
  }

  /// Remove a single model value.
  void remove(T value) {
    // XXX should we set the notifier value to null before removing it?
    // XXX this._values[value.primaryKey].value = null

    this._values.remove(value.primaryKey);
    this.notifyListeners();
  }

  /// Get the model notifier for the given model value.
  N getNotifierFor(T value) {
    // TODO: this._modelNotifiers.containsKey(value.primaryKey)
    return this._values[value.primaryKey];
  }
}
