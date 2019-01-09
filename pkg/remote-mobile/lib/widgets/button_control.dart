import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/stores/control.dart';
import 'package:remote/models/models.dart';

class ButtonControlWidget extends StatefulWidget {
  final Repository repository;
  final String controlUuid;

  ButtonControlWidget({Key key, @required this.repository, @required this.controlUuid}):
    super(key: key);

  @override
  _ButtonControlWidgetState createState() => _ButtonControlWidgetState();
}

class _ButtonControlWidgetState extends State<ButtonControlWidget> {
  ControlNotifier _notifier;

  void onControlChanged() {
    this.setState(() {});
  }

  void onClick() {
    // TODO: implement me
  }

  @override
  void initState() {
    super.initState();

    this._notifier = this.widget.repository.controls.getNotifierByKey(this.widget.controlUuid);
    this._notifier.addListener(this.onControlChanged);
  }

  @override
  void didUpdateWidget(ButtonControlWidget oldWidget) {
    super.didUpdateWidget(oldWidget);

    this._notifier.removeListener(this.onControlChanged);
    this._notifier = this.widget.repository.controls.getNotifierByKey(this.widget.controlUuid);
    this._notifier.addListener(this.onControlChanged);
  }

  @override
  void dispose() {
    this._notifier.removeListener(this.onControlChanged);
    this._notifier.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final buttonControl = this._notifier.value as ButtonControl;
    return Container(
      child: Expanded(
        child: RaisedButton(
          onPressed: this.onClick,
          child: Text(buttonControl.title)
        )
      ),
    );
  }
}
