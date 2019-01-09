import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/stores/control_set.dart';

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
    return Card(
      child: Container(
        padding: const EdgeInsets.all(8.0),
        child: Row(
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
        ),
      ),
    );
  }
}
