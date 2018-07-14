import 'package:flutter/material.dart';

class StatusIndicator extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        children: [
          CircularProgressIndicator(),
          Expanded(
            child: Container(
              padding: const EdgeInsets.only(left: 16.0),
              child: Text(
                "Running 'More Light'...",
                style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.75),
              ),
            ),
          ),
          IconButton(
            icon: Icon(Icons.cancel),
            color: Color.fromRGBO(196, 0, 0, 1.0),
            tooltip: "Cancel",
            onPressed: () {},
          ),
        ],
      ),
    );
  }
}
