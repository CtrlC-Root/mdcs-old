import 'package:flutter/material.dart';

class ActionList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: 5,
      itemBuilder: (context, index) {
        return Card(
          child: Text("Action $index"),
        );
      },
    );
  }
}
