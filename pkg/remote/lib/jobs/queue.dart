import 'dart:async';
import 'dart:isolate';
import 'package:remote/jobs/job.dart';

/// Isolate entry point for running queue jobs.
/// https://flutter.io/flutter-for-ios/#how-do-you-move-work-to-a-background-thread
void jobQueueRun(SendPort sendPort) async {
  // create a receive port for incoming jobs and send it's send port to the main process
  ReceivePort receivePort = ReceivePort();
  sendPort.send(receivePort.sendPort);

  // receive jobs from the parent process and run them
  await for (List<dynamic> message in receivePort) {
    final Job job = message[0];
    final SendPort replyPort = message[1];

    try {
      await job.run();
    } on Exception catch (e) {
      job.fail(e);
    } catch (e) {
      job.fail(Exception(e.toString()));
    }

    replyPort.send(job);
  }
}

/// Job queue state.
enum JobQueueState {
  initial,
  starting,
  running,
  stopping,
  stopped
}

/// A queue for running Job(s) in the background.
/// https://flutter.io/flutter-for-ios/#how-do-you-move-work-to-a-background-thread
/// https://docs.flutter.io/flutter/foundation/compute.html
class JobQueue {
  JobQueueState _state;
  ReceivePort _receivePort;
  SendPort _sendPort;
  Isolate _isolate;

  JobQueue() :
    this._state = JobQueueState.initial,
    this._receivePort = ReceivePort(),
    this._sendPort = null,
    this._isolate = null;

  Future start() async {
    assert(this._state == JobQueueState.initial);

    this._state = JobQueueState.starting;
    return await Isolate.spawn(jobQueueRun, this._receivePort.sendPort)
      .then((Isolate isolate) {
        this._isolate = isolate;
        return this._receivePort.first;
      })
      .then((dynamic sendPort) {
        this._sendPort = sendPort as SendPort;
        this._state = JobQueueState.running;
      })
      .catchError((dynamic e) {
        this._state = JobQueueState.stopped;
        throw Exception('failed to start isolate for job queue: ${e.toString()}');
      });
  }

  void stop() {
    assert(this._state == JobQueueState.running);

    this._state = JobQueueState.stopping;
    this._receivePort.close();
    this._isolate.kill(priority: Isolate.immediate);

    this._state = JobQueueState.stopped;
    this._receivePort = null;
    this._sendPort = null;
    this._isolate = null;
  }

  Future<T> run<T extends Job>(T job) async {
    assert(this._state == JobQueueState.running);

    ReceivePort response = ReceivePort();
    this._sendPort.send([job, response.sendPort]);
    final T result = await response.first;
    return result;
  }
}
