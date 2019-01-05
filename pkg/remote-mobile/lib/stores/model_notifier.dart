import 'package:flutter/foundation.dart';
import 'package:remote/models/model.dart';

/// Abstract base class for model notifiers.
abstract class ModelNotifier<T extends Model> extends ValueNotifier<T> {
  ModelNotifier(T initialValue) : super(initialValue);
}
