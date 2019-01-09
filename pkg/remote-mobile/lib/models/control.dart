import 'package:remote/models/model.dart';

/// Control type.
enum ControlType {
  none,
  button,
  color
}

/// A generic control.
class Control extends Model {
  final String uuid;
  final String controlSetUuid;
  final String name;
  final ControlType type;
  final String description;

  Control({this.uuid, this.controlSetUuid, this.name, this.type, this.description});

  Control.fromJSON(Map<String, dynamic> data) :
    this.uuid = data['uuid'] as String,
    this.controlSetUuid = data['controlset_uuid'] as String,
    this.name = data['name'] as String,
    this.type = Control.parseControlType(data['type'] as String),
    this.description = data['description'] as String;

  static ControlType parseControlType(String value) {
    switch (value.toLowerCase()) {
      case 'none': return ControlType.none;
      case 'button': return ControlType.button;
      case 'color': return ControlType.color;
      default: throw Exception('unknown control type: $value');
    }
  }

  @override
  String get primaryKey => this.uuid;
}
