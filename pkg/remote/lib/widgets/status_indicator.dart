import 'package:flutter/material.dart';

class StatusIndicator extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        CircularProgressIndicator(),
        Expanded(
          child: Text("Running 'More Action' ..."),
        ),
      ]
    );
  }
}
