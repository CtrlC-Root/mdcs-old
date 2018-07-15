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
        Action action = actions[index];
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
      },
    );
  }
}