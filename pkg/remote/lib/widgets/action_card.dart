import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/stores/action.dart';

class ActionCard extends StatefulWidget {
  final Repository repository;
  final String actionUuid;

  ActionCard({Key key, @required this.repository, @required this.actionUuid}) : super(key: key);

  @override
  _ActionCardState createState() => _ActionCardState();
}

class _ActionCardState extends State<ActionCard> {
  ActionNotifier _notifier;

  void onActionChanged() {
    this.setState(() {});
  }

  @override
  void initState() {
    super.initState();

    this._notifier = this.widget.repository.actions.getNotifierByKey(this.widget.actionUuid);
    this._notifier.addListener(this.onActionChanged);
  }

  @override
  void didUpdateWidget(ActionCard oldWidget) {
    super.didUpdateWidget(oldWidget);

    this._notifier.removeListener(this.onActionChanged);
    this._notifier = this.widget.repository.actions.getNotifierByKey(this.widget.actionUuid);
    this._notifier.addListener(this.onActionChanged);
  }

  @override
  void dispose() {
    this._notifier.removeListener(this.onActionChanged);
    this._notifier.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final action = this._notifier.value;
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
                    action.title,
                    style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.25),
                  ),
                  Text(
                    action.description,
                    style: DefaultTextStyle.of(context).style.copyWith(fontWeight: FontWeight.w300),
                  ),
                ],
              ),
            ),
            IconButton(
              icon: Icon(Icons.play_arrow),
              tooltip: "Run",
              onPressed: () {},
            ),
            IconButton(
              icon: Icon(Icons.details),
              color: Color.fromRGBO(0, 196, 0, 1.0),
              tooltip: "Details",
              onPressed: () {},
            ),
          ],
        )
      ),
    );
  }
}
