import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:remote/models/models.dart';
import 'package:remote/jobs/job.dart';

class FetchTaskJob extends Job {
  final Uri _api;
  final String _primaryKey;
  Task _task;

  FetchTaskJob(Uri api, String primaryKey) : this._api = api, this._primaryKey = primaryKey, this._task = null, super();

  @override
  Future run() async {
    final client = http.Client();

    // retrieve task
    final taskUri = this._api.replace(path: '${this._api.path}/task/${this._primaryKey}');
    final response = await client.get(taskUri.toString());

    if (response.statusCode != 200) {
      this.fail(Exception('failed to retrieve task: ${this._primaryKey}'));
      return;
    }

    // parse task
    final Map<String, dynamic> taskData = json.decode(response.body);
    this._task = Task.fromJSON(taskData);

    // done
    this.complete();
  }

  String get primaryKey => this._primaryKey;

  Task get task {
    assert(this.state == JobState.completed);
    return this._task;
  }
}
