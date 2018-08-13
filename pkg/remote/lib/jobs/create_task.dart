import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:remote/models/models.dart';
import 'package:remote/jobs/job.dart';

class CreateTaskJob extends Job {
  final Uri _api;
  final Action _action;
  Task _task;

  CreateTaskJob(Uri api, Action action) : this._api = api, this._action = action, this._task = null, super();

  @override
  Future run() async {
    final client = http.Client();

    // create task
    final taskUri = this._api.replace(path: '${this._api.path}/task/');
    final createResponse = await client.post(
      taskUri.toString(),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'action_uuid': this._action.uuid}));

    if (createResponse.statusCode != 200) {
      this.fail(Exception('failed to create task for action ${this._action.uuid}: ${createResponse.body}'));
      return;
    }

    // parse task
    final Map<String, dynamic> taskData = json.decode(createResponse.body);
    this._task = Task.fromJSON(taskData);

    // done
    this.complete();
  }

  Action get action => this._action;

  Task get task {
    assert(this.state == JobState.completed);
    return this._task;
  }
}
