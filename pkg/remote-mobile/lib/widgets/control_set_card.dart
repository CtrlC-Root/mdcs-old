import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/stores/control_set.dart';
import 'package:remote/models/models.dart';

class ControlSetCard extends StatefulWidget {
  final Repository repository;
  final String controlSetUuid;

  ControlSetCard({Key key, @required this.repository, @required this.controlSetUuid}) : super(key: key);

  @override
  _ControlSetCardState createState() => _ControlSetCardState();
}

class _ControlSetCardState extends State<ControlSetCard> {
  ControlSetNotifier _notifier;

  void onControlSetChanged() {
    this.setState(() {});
  }

  void onButtonControlClick() {
    // TODO
  }

  @override
  void initState() {
    super.initState();

    this._notifier = this.widget.repository.controlSets.getNotifierByKey(this.widget.controlSetUuid);
    this._notifier.addListener(this.onControlSetChanged);
  }

  @override
  void didUpdateWidget(ControlSetCard oldWidget) {
    super.didUpdateWidget(oldWidget);

    this._notifier.removeListener(this.onControlSetChanged);
    this._notifier = this.widget.repository.controlSets.getNotifierByKey(this.widget.controlSetUuid);
    this._notifier.addListener(this.onControlSetChanged);
  }

  @override
  void dispose() {
    this._notifier.removeListener(this.onControlSetChanged);
    this._notifier.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final controlSet = this._notifier.value;
    final headerRow = Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                controlSet.name,
                style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.25),
              ),
              Text(
                controlSet.description,
                style: DefaultTextStyle.of(context).style.copyWith(fontWeight: FontWeight.w300),
              ),
            ],
          ),
        ),
        IconButton(
          icon: Icon(Icons.details),
          color: Color.fromRGBO(0, 196, 0, 1.0),
          tooltip: "Details",
          onPressed: () {},
        ),
      ],
    );

    // XXX: should the repository or store help here?
    final controls = this.widget.repository.controls.values
      .where((Control control) => control.controlSetUuid == controlSet.uuid)
      .toList();

    // XXX: sort order?
    // controls.sort((Control a, Control b) => a.name.compareTo(b.name));

    final controlRows = controls.map((Control control) {
      switch (control.type) {
        case ControlType.button:
          final buttonControl = control as ButtonControl;
          return Row(
            children: [
              Expanded(
                child: RaisedButton(
                  onPressed: this.onButtonControlClick,
                  child: Text(buttonControl.title)
                )
              )
            ]
          );

        case ControlType.color:
          // TODO: implement a color picker widget

        case ControlType.none:
          return Row(
            children: [
              Expanded(
                child: Text(control.description)
              )
            ],
          );
      }
    });

    // XXX: this feels dirty
    List<Widget> widgets = List<Widget>();
    widgets.add(headerRow);
    widgets.addAll(controlRows);

    return Card(
      margin: const EdgeInsets.all(8.0),
      child: Container(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          children: widgets,
        )
      )
    );
  }
}
