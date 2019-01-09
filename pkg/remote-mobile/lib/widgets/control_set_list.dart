import 'package:flutter/material.dart';
import 'package:remote/repository.dart';
import 'package:remote/models/control_set.dart';
import 'package:remote/widgets/control_set_card.dart';

class ControlSetList extends StatefulWidget {
  final Repository repository;

  ControlSetList({Key key, @required this.repository}) : super(key: key);

  @override
  _ControlSetListState createState() => _ControlSetListState();
}

class _ControlSetListState extends State<ControlSetList> {
  void onControlSetsChanged() {
    this.setState(() {});
  }

  Future onRefreshList() {
    return this.widget.repository.fetchAll();
  }

  @override
  void initState() {
    super.initState();

    this.widget.repository.controlSets.addListener(this.onControlSetsChanged);
  }

  @override
  void didUpdateWidget(ControlSetList oldWidget) {
    super.didUpdateWidget(oldWidget);

    oldWidget.repository.controlSets.removeListener(this.onControlSetsChanged);
    this.widget.repository.controlSets.addListener(this.onControlSetsChanged);
  }

  @override
  void dispose() {
    this.widget.repository.controlSets.removeListener(this.onControlSetsChanged);

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final List<ControlSet> controlSets = this.widget.repository.controlSets.values;
    return RefreshIndicator(
      onRefresh: this.onRefreshList,
      child: ListView.builder(
        physics: const AlwaysScrollableScrollPhysics(),
        itemCount: controlSets.length,
        itemBuilder: (context, index) {
          return ControlSetCard(
            repository: this.widget.repository,
            controlSetUuid: controlSets[index].uuid
          );
        },
      )
    );
  }
}
