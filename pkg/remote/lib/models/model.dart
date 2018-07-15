import 'package:meta/meta.dart';

/// Abstract base class for models.
@immutable
abstract class Model {
  /// Primary key field value.
  String get primaryKey;
}
