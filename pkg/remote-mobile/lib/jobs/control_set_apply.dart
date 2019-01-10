import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:remote/models/models.dart';
import 'package:remote/jobs/job.dart';

class ControlSetApplyJob extends Job {
  final Uri _api;
  final ControlSet _controlSet;
  final Map<String, ControlValue> _input;
  Task _task;

  ControlSetApplyJob(this._api, this._controlSet, this._input):
    this._task = null,
    super();

  @override
  Future run() async {
    final client = http.Client();

    // convert the control values to their JSON serializable representations
    final inputData = this._input.map((String name, ControlValue value) => MapEntry(name, value.toData()));

    // create task
    final taskUri = this._api.replace(path: '${this._api.path}/controlset/${this._controlSet.uuid}/apply');
    final response = await client.post(
      taskUri.toString(),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(inputData));

    if (response.statusCode != 200) {
      this.fail(Exception('failed to apply control set ${this._controlSet.uuid}: ${response.body}'));
      return;
    }

    // parse task
    final Map<String, dynamic> taskData = json.decode(response.body);
    this._task = Task.fromJSON(taskData);

    // done
    this.complete();
  }

  ControlSet get controlSet => this._controlSet;

  Map<String, ControlValue> get input => this._input;

  Task get task {
    assert(this.state == JobState.completed);
    return this._task;
  }
}
