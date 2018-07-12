import 'package:remote/models/models.dart';
import 'package:remote/stores/stores.dart';

class Repository {
  final ActionStore actions = ActionStore();

  Repository() {
    // TODO: remove this debugging code
    actions.values = [
      Action(uuid: "one", title: "More Light", content: "more_light()"),
      Action(uuid: "two", title: "Less Light", content: "less_light()"),
    ];
  }
}
