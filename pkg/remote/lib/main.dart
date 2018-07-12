import 'package:flutter/material.dart';
import 'package:remote/models/models.dart';

void main() => runApp(RemoteApp());

class Store extends ValueNotifier<Action> {
  Store() : super(Action(uuid: "", title: "Example", content: ""));

  void updateAction({String uuid, String title, String content}) {
    this.value = Action(
      uuid: uuid ?? this.value.uuid,
      title: title ?? this.value.title,
      content: content ?? this.value.content);
  }
}

class RemoteApp extends StatelessWidget {
  final Store store = Store();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Remote Control',
      home: Scaffold(
        appBar: AppBar(
          title: Text('Remote Control'),
        ),
        body: Row(
          children: [
            ActionDetail(store: this.store),
            ActionTest(store: this.store),
          ]
        ),
      ),
    );
  }
}

/// Dummy widget to test updating the Action through the Store.
class ActionTest extends StatelessWidget {
  final Store store;

  ActionTest({Key key, @required this.store}) : super(key: key);

  void onPress() {
    this.store.updateAction(title: "Testing!");
  }

  @override
  Widget build(BuildContext context) {
    return RaisedButton(
      child: Text("Change It!"),
      onPressed: this.onPress,
    );
  }
}

class ActionDetail extends StatefulWidget {
  final Store store;

  ActionDetail({Key key, @required this.store}) : super(key: key);

  @override
  _ActionDetailState createState() => _ActionDetailState();
}

class _ActionDetailState extends State<ActionDetail> {
  @override
  void initState() {
    super.initState();

    this.widget.store.addListener(this.onActionChange);
  }

  @override
  void didUpdateWidget(ActionDetail oldWidget) {
    super.didUpdateWidget(oldWidget);

    if (oldWidget.store != this.widget.store) {
      oldWidget.store.removeListener(this.onActionChange);
      this.widget.store.addListener(this.onActionChange);
    }
  }

  @override
  void dispose() {
    this.widget.store.removeListener(this.onActionChange);

    super.dispose();
  }

  void onActionChange() {
    this.setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Text("${this.widget.store.value.title}");
  }
}
