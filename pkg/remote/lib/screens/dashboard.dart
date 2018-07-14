import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/widgets/widgets.dart';

class DashboardScreen extends StatelessWidget {
  final Repository repository;

  DashboardScreen({Key key, @required this.repository}) : super(key: key);

  void onNavigateSettings() {
    // TODO: do something
  }

  void onNewAction() {
    // TODO: do something
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Remote Control'),
        actions: [
          IconButton(
            icon: Icon(Icons.settings),
            tooltip: "Settings",
            onPressed: this.onNavigateSettings,
          ),
        ],
      ),
      body: Column(
        children: [
          StatusIndicator(),
          Expanded(
            child: ActionList(repository: repository),
          ),
        ],
      ),
      floatingActionButton: IconButton(
        icon: Icon(Icons.add_circle),
        iconSize: 48.0,
        color: Color.fromRGBO(0, 0, 196, 1.0),
        tooltip: "New",
        onPressed: this.onNewAction,
      ),
      // floatingActionButtonLocation: FloatingActionButtonLocation.endFloat,
    );
  }
}
