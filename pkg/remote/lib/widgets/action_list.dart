import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/models/action.dart';

class ActionList extends StatefulWidget {
  final Repository repository;

  ActionList({Key key, @required this.repository}) : super(key: key);

  @override
  _ActionListState createState() => _ActionListState();
}

class _ActionListState extends State<ActionList> {
  void onActionsChanged() {
    this.setState(() {});
  }

  @override
  void initState() {
    super.initState();

    this.widget.repository.actions.addListener(this.onActionsChanged);
  }

  @override
  void didUpdateWidget(ActionList oldWidget) {
    super.didUpdateWidget(oldWidget);

    oldWidget.repository.actions.removeListener(this.onActionsChanged);
    this.widget.repository.actions.addListener(this.onActionsChanged);
  }

  @override
  void dispose() {
    this.widget.repository.actions.removeListener(this.onActionsChanged);

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    List<Action> actions = this.widget.repository.actions.values;
    return ListView.builder(
      itemCount: actions.length,
      itemBuilder: (context, index) {
        return Card(
          child: Text("Action ${actions[index].title}"),
        );
      },
    );
  }
}
