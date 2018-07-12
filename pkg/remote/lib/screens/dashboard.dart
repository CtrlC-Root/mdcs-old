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
        ]
      ),
    );
  }
}
