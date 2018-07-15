import 'package:remote/models/model.dart';

/// A runnable action.
class Action extends Model {
    String uuid;
    String title;
    String description;
    String content;

    Action({this.uuid, this.title, this.description, this.content});

    static Action fromJSON(Map<String, dynamic> data) {
      return Action(
        uuid: data['uuid'] as String,
        title: data['title'] as String,
        description: data['description'] as String,
        content: data['content'] as String,
      );
    }
}
