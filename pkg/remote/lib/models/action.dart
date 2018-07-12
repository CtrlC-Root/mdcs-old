import 'package:remote/models/model.dart';

/// A runnable action.
class Action extends Model {
    String uuid;
    String title;
    String content;

    Action({this.uuid, this.title, this.content});
}
