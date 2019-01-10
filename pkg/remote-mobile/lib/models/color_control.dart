import 'package:remote/models/control.dart';

/// A color control.
class ColorControl extends Control {
  ColorControl({String uuid, String controlSetUuid, String name, String description}):
    super(
      uuid: uuid,
      controlSetUuid: controlSetUuid,
      name: name,
      type: ControlType.color,
      description: description);

  ColorControl.fromJSON(Map<String, dynamic> data, {String controlSetUuid}):
    super(
      uuid: data['uuid'] as String,
      controlSetUuid: controlSetUuid != null ? controlSetUuid : data['controlset_uuid'] as String,
      name: data['name'] as String,
      type: Control.parseControlType(data['type'] as String),
      description: data['description'] as String)
  {
    assert(this.type == ControlType.color);
  }
}

/// A color control value.
class ColorValue extends ControlValue {
  final int red;
  final int green;
  final int blue;

  ColorValue({this.red, this.green, this.blue}): super();
  ColorValue.fromJSON(Map<String, dynamic> data):
    this.red = int.parse(data['red'] as String),
    this.green = int.parse(data['green'] as String),
    this.blue = int.parse(data['blue'] as String),
    super();

  @override
  Map<String, dynamic> toData() => {'red': this.red, 'green': this.green, 'blue': this.blue};
}
