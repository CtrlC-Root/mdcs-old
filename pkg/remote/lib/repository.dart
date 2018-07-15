import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';
import 'package:remote/models/models.dart';
import 'package:remote/stores/stores.dart';

List<Action> parseActions(List<Map<String, dynamic>> data) {
  return data.map((Map<String, dynamic> actionData) => Action.fromJSON(actionData)).toList();
}

class Repository {
  final ActionStore actions = ActionStore();

  Future<List<Action>> fetchActions(http.Client client) async {
    final actionUri = Uri(scheme: 'http', host: 'localhost', port: 5000, path: '/action/');
    final response = await client.get(actionUri.toString());
    if (response.statusCode != 200) {
      throw Exception("Failed to fetch actions from backend!");
    }

    final List<Map<String, dynamic>> data = json.decode(response.body).cast<Map<String, dynamic>>();
    return compute(parseActions, data);
    // return this.parseActions(data);
  }

  void syncWithBackend() {
    final client = http.Client();
    this.fetchActions(client).then((List<Action> actions) {
      this.actions.values = actions;
    }).catchError((error) {
      debugPrint(error.toString());
    });
  }
}
