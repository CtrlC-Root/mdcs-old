import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/widgets/widgets.dart';

class DashboardScreen extends StatelessWidget {
  final Repository repository;

  DashboardScreen({Key key, @required this.repository}) : super(key: key);

  void onNavigateSettings() {
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
          StatusIndicator(repository: repository),
          Expanded(
            child: Text('TODO'),
          ),
        ],
      ),
    );
  }
}
