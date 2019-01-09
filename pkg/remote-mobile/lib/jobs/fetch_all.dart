import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:remote/models/models.dart';
import 'package:remote/jobs/job.dart';

class FetchAllJob extends Job {
  final Uri _api;
  List<ControlSet> _controlSets;
  List<Control> _controls;
  List<Task> _tasks;

  FetchAllJob(Uri api):
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
    final List<Map<String, dynamic>> controlSetsData = json.decode(controlSetResponse.body).cast<Map<String, dynamic>>();

    for (var controlSetData in controlSetsData) {
      final controlSet = ControlSet.fromJSON(controlSetData);
      this._controlSets.add(controlSet);

      // parse controls
      for (var controlData in controlSetData['controls']) {
        final type = Control.parseControlType(controlData['type']);
        switch (type) {
          case ControlType.button:
            this._controls.add(ButtonControl.fromJSON(controlData, controlSetUuid: controlSet.uuid));
            break;
          case ControlType.color:
            this._controls.add(ColorControl.fromJSON(controlData, controlSetUuid: controlSet.uuid));
            break;
          case ControlType.none:
            // XXX: this shouldn't happen, what do we do here?
            this._controls.add(Control.fromJSON(controlData, controlSetUuid: controlSet.uuid));
            break;
        }
      }
    }

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
