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
    if (this._values.containsKey(value.primaryKey)) {
      throw Exception('store already contains value with key: ${value.primaryKey}');
    }

    this._values[value.primaryKey] = this.createModelNotifier(value);
    this.notifyListeners();
  }

  /// Remove a single model value.
  void remove(String primaryKey) {
    if (!this._values.containsKey(primaryKey)) {
      throw Exception('store does not contain value with key: $primaryKey');
    }

    // XXX this._values[primaryKey].value = null;
    this._values.remove(primaryKey);
    this.notifyListeners();
  }

  /// Get the model notifier for the model with the given primary key.
  N getNotifierByKey(String primaryKey) {
    // TODO: this._values.containsKey(primaryKey)
    return this._values[primaryKey];
  }

  /// Get the model with the given primary key.
  T getValueByKey(String primaryKey) {
    // TODO: this._values.containsKey(primaryKey)
    return this._values[primaryKey].value;
  }
}
