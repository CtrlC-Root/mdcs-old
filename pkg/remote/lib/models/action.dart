import 'package:remote/models/model.dart';

/// A runnable action.
class Action extends Model {
    final String uuid;
    final String title;
    final String description;
    final String content;

    Action({this.uuid, this.title, this.description, this.content});

    Action.fromJSON(Map<String, dynamic> data) :
      this.uuid = data['uuid'] as String,
      this.title = data['title'] as String,
      this.description = data['description'] as String,
      this.content = data['content'] as String;

    @override
    String get primaryKey => this.uuid;
}
