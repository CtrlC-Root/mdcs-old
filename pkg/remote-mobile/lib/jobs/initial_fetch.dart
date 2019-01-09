import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:remote/models/models.dart';
import 'package:remote/jobs/job.dart';

class InitialFetchJob extends Job {
  final Uri _api;
  List<ControlSet> _controlSets;
  List<Control> _controls;
  List<Task> _tasks;

  InitialFetchJob(Uri api):
    this._api = api,
    this._controlSets = List<ControlSet>(),
    this._controls = List<Control>(),
    this._tasks = List<Task>(),
    super();

  @override
  Future run() async {
    final client = http.Client();

    // retrieve control sets
    final controlSetUri = this._api.replace(path: '${this._api.path}/controlset/');
    final controlSetResponse = await client.get(controlSetUri.toString());

    if (controlSetResponse.statusCode != 200) {
      this.fail(Exception('failed to retrieve control sets'));
      return;
    }

    // parse control sets
    final List<Map<String, dynamic>> controlSetData = json.decode(controlSetResponse.body).cast<Map<String, dynamic>>();
    this._controlSets = controlSetData.map((Map<String, dynamic> data) => ControlSet.fromJSON(data)).toList();

   // retrieve controls
    final controlUri = this._api.replace(path: '${this._api.path}/control/');
    final controlResponse = await client.get(controlUri.toString());

    if (controlResponse.statusCode != 200) {
      this.fail(Exception('failed to retrieve control sets'));
      return;
    }

    // parse control sets
    final List<Map<String, dynamic>> controlData = json.decode(controlResponse.body).cast<Map<String, dynamic>>();
    this._controls = controlData.map((Map<String, dynamic> data) => Control.fromJSON(data)).toList();

    // retrieve tasks
    final taskUri = this._api.replace(path: '${this._api.path}/task/');
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

  List<ControlSet> get controlSets {
    assert(this.state == JobState.completed);
    return this._controlSets;
  }

  List<Control> get controls {
    assert(this.state == JobState.completed);
    return this._controls;
  }

  List<Task> get tasks {
    assert(this.state == JobState.completed);
    return this._tasks;
  }
}
