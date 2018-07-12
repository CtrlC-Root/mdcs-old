import 'package:flutter/material.dart';
import 'package:remote/widgets/widgets.dart';

class DashboardScreen extends StatelessWidget {
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
            child: ActionList(),
          ),
        ]
      ),
    );
  }
}
