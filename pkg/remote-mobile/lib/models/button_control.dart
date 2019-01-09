import 'package:remote/models/control.dart';

/// A button control.
class ButtonControl extends Control {
  final String title;

  ButtonControl({String uuid, String controlSetUuid, String name, String description, this.title}):
    super(
      uuid: uuid,
      controlSetUuid: controlSetUuid,
      name: name,
      type: ControlType.button,
      description: description);

  ButtonControl.fromJSON(Map<String, dynamic> data, {String controlSetUuid}):
    this.title = data['button']['title'] as String,
    super(
      uuid: data['uuid'] as String,
      controlSetUuid: controlSetUuid != null ? controlSetUuid : data['controlset_uuid'] as String,
      name: data['name'] as String,
      type: Control.parseControlType(data['type'] as String),
      description: data['description'] as String)
  {
    assert(this.type == ControlType.button);
  }
}
