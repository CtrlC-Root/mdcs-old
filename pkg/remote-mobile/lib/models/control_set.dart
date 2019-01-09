import 'package:remote/models/model.dart';

/// Control set configuration type.
enum ConfigType {
  lua
}

/// A set of controls for controlling a group of related devices.
class ControlSet extends Model {
  final String uuid;
  final String name;
  final String description;
  final ConfigType configType;
  final String config;

  ControlSet({this.uuid, this.name, this.description, this.configType, this.config});

  ControlSet.fromJSON(Map<String, dynamic> data) :
    this.uuid = data['uuid'] as String,
    this.name = data['name'] as String,
    this.description = data['description'] as String,
    this.configType = ControlSet.parseConfigType(data['config_type'] as String),
    this.config = data['config'] as String;

  static ConfigType parseConfigType(String value) {
    switch (value.toLowerCase()) {
      case 'lua': return ConfigType.lua;
      default: throw Exception('unknown config type: $value');
    }
  }

  @override
  String get primaryKey => this.uuid;
}
