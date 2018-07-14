import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/widgets/widgets.dart';

class DashboardScreen extends StatelessWidget {
  final Repository repository;

  DashboardScreen({Key key, @required this.repository}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Remote Control'),
      ),
      body: Column(
        children: [
          StatusIndicator(),
          Expanded(
            child: ActionList(repository: repository),
          ),
          DashboardControls(),
        ],
      ),
    );
  }
}

class DashboardControls extends StatelessWidget {
  void onNewAction() {
    // TODO: do something
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.end,
      children: [
        IconButton(
          icon: Icon(Icons.add_circle),
          iconSize: 48.0,
          color: Color.fromRGBO(0, 0, 196, 1.0),
          tooltip: "New",
          onPressed: this.onNewAction,
        ),
      ],
    );
  }
}
