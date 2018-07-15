import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:remote/models/models.dart';
import 'package:remote/jobs/job.dart';

class InitialFetchJob extends Job {
  final Uri _api;
  List<Action> _actions;
  List<Task> _tasks;

  InitialFetchJob(Uri api) : this._api = api, this._actions = List<Action>(), this._tasks = List<Task>(), super();

  @override
  Future run() async {
    final client = http.Client();

    // retrieve actions
    final actionUri = this._api.replace(path: '/action/');
    final actionResponse = await client.get(actionUri.toString());

    if (actionResponse.statusCode != 200) {
      this.fail(Exception('failed to retrieve actions'));
      return;
    }

    // parse actions
    final List<Map<String, dynamic>> actionsData = json.decode(actionResponse.body).cast<Map<String, dynamic>>();
    this._actions = actionsData.map((Map<String, dynamic> data) => Action.fromJSON(data)).toList();

    // retrieve tasks
    final taskUri = this._api.replace(path: '/task/');
    final taskResponse = await client.get(taskUri.toString());

    if (taskResponse.statusCode != 200) {
      this.fail(Exception('failed to retrieve tasks'));
      return;
    }

    // parse tasks
    final List<Map<String, dynamic>> tasksData = json.decode(taskResponse.body).cast<Map<String, dynamic>>();
    this._tasks = tasksData.map((Map<String, dynamic> data) => Task.fromJSON(data)).toList();

    // done
    this.complete();
  }

  List<Action> get actions {
    assert(this.state == JobState.completed);
    return this._actions;
  }

  List<Task> get tasks {
    assert(this.state == JobState.completed);
    return this._tasks;
  }
}
