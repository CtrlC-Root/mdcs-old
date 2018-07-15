import 'dart:async';
import 'package:meta/meta.dart';

enum JobState {
  pending,
  completed,
  failed
}

abstract class Job {
  Exception _error;
  JobState _state;

  Job() : this._error = null, this._state = JobState.pending;

  JobState get state => this._state;

  Exception get error {
    assert(this._state == JobState.failed);
    return this._error;
  }

  /// Do the work this Job represents. This is called in the background isolate.
  Future run();

  /// Mark this job as completed.
  @mustCallSuper
  void complete() {
    assert(this._state == JobState.pending);
    this._state = JobState.completed;
  }

  /// Mark this job as failed.
  @mustCallSuper
  void fail(Exception error) {
    assert(this._state == JobState.pending);
    this._error = error;
    this._state = JobState.failed;
  }
}
