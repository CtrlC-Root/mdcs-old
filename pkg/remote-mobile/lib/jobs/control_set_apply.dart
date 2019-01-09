import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:remote/models/models.dart';
import 'package:remote/jobs/job.dart';

class ApplyControlSetJob extends Job {
  final Uri _api;
  final ControlSet _controlSet;
  Task _task;

  ApplyControlSetJob(Uri api, ControlSet controlSet):
    this._api = api,
    this._controlSet = controlSet,
    this._task = null,
    super();

  @override
  Future run() async {
    final client = http.Client();

    // create task
    final taskUri = this._api.replace(path: '${this._api.path}/controlset/${this._controlSet.uuid}/apply');
    final response = await client.post(
      taskUri.toString(),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'todo': {'clicked': true}}));  // TODO: inputs go here

    if (response.statusCode != 200) {
      this.fail(Exception('failed to create task for control set ${this._controlSet.uuid}: ${response.body}'));
      return;
    }

    // parse task
    final Map<String, dynamic> taskData = json.decode(response.body);
    this._task = Task.fromJSON(taskData);

    // done
    this.complete();
  }

  ControlSet get controlSet => this._controlSet;

  Task get task {
    assert(this.state == JobState.completed);
    return this._task;
  }
}
