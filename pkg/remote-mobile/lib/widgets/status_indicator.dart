import 'dart:async';
import 'package:flutter/material.dart';
import 'package:remote/models/models.dart';
import 'package:remote/stores/stores.dart';
import 'package:remote/repository.dart';

class StatusIndicator extends StatefulWidget {
  final Repository repository;

  StatusIndicator({Key key, @required this.repository}) : super(key: key);

  @override
  _StatusIndicatorState createState() => _StatusIndicatorState();
}

class _StatusIndicatorState extends State<StatusIndicator> {
  Timer _refresh;
  TaskNotifier _notifier;

  Task get _task => _notifier?.value;

  Task pickTask(List<Task> tasks) {
    tasks.sort((a, b) => a.modified.compareTo(b.modified));

    final running = tasks.where((Task task) => (task.state == TaskState.running));
    if (running.isNotEmpty) {
      return running.last;
    }

    final pending = tasks.where((Task task) => (task.state == TaskState.pending));
    if (pending.isNotEmpty) {
      return pending.last;
    }

    final cutoff = DateTime.now().subtract(Duration(seconds: 5));
    final done = tasks.where((Task task) => task.modified.isAfter(cutoff));

    if (done.isEmpty) {
      return null;
    }

    return done.last;
  }

  void onTasksChanged() {
    this.setState(() {
      this._refresh?.cancel();
      this._notifier?.removeListener(this.onTaskChanged);
      this._notifier = null;

      final task = this.pickTask(this.widget.repository.tasks.values);
      if (task == null) {
        return;
      }

      this._notifier = this.widget.repository.tasks.getNotifierByKey(task.primaryKey);
      this._notifier.addListener(this.onTaskChanged);
      this._refresh = Timer(Duration(seconds: 2), this.onRefreshTimer);
    });
  }

  void onRefreshTimer() {
    this.widget.repository.fetchPendingTasks()
      .then((dynamic tasks) {
        // this._refresh = Timer(Duration(seconds: 2), this.onRefreshTimer);
        this.onTasksChanged();
      });
  }

  void onTaskChanged() {
    this.setState(() {});
  }

  @override
  void initState() {
    super.initState();

    this.widget.repository.tasks.addListener(this.onTasksChanged);
    this.onTasksChanged();
  }

  @override
  void didUpdateWidget(StatusIndicator oldWidget) {
    super.didUpdateWidget(oldWidget);

    oldWidget.repository.tasks.removeListener(this.onTasksChanged);
    this.widget.repository.tasks.addListener(this.onTasksChanged);
    this.onTasksChanged();
  }

  @override
  void dispose() {
    this.widget.repository.tasks.removeListener(this.onTasksChanged);
    this._refresh?.cancel();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (this._task == null) {
      return Container();
    }

    String statusText;
    Widget statusWidget;
    switch (this._task.state) {
      case TaskState.pending:
      case TaskState.running:
        statusText = "Running";
        statusWidget = CircularProgressIndicator();
        break;

      case TaskState.completed:
        statusText = "Finished";
        statusWidget = Icon(Icons.check_circle, color: Color.fromRGBO(0, 196, 0, 1.0), size: 48.0);
        break;

      case TaskState.cancelled:
      case TaskState.failed:
        statusText = "Failed";
        statusWidget = Icon(Icons.error, color: Color.fromRGBO(196, 0, 0, 1.0), size: 48.0);
        break;
    }

    return Container(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        children: [
          statusWidget,
          Expanded(
            child: Container(
              padding: const EdgeInsets.only(left: 16.0),
              child: Text(
                statusText,
                style: DefaultTextStyle.of(context).style.apply(fontSizeFactor: 1.75),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
