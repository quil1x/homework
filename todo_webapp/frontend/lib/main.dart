import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(const TodoApp());

class Todo {
  final int id;
  String title;
  bool isDone;
  Todo({required this.id, required this.title, this.isDone = false});
  factory Todo.fromJson(Map<String, dynamic> json) {
    return Todo(id: json['id'], title: json['title'], isDone: json['is_done']);
  }
}

class TodoApp extends StatelessWidget {
  const TodoApp({super.key});
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(title: 'TODO', home: TodoPage(), debugShowCheckedModeBanner: false);
  }
}

class TodoPage extends StatefulWidget {
  const TodoPage({super.key});
  @override
  State<TodoPage> createState() => _TodoPageState();
}

class _TodoPageState extends State<TodoPage> {
  final _url = 'http://localhost:8000/todos/';
  List<Todo> _todos = [];
  final _controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetch();
  }

  Future<void> _fetch() async {
    final r = await http.get(Uri.parse(_url));
    if (r.statusCode == 200) {
      setState(() => _todos = (jsonDecode(r.body) as List).map((e) => Todo.fromJson(e)).toList());
    }
  }

  Future<void> _add() async {
    if (_controller.text.isEmpty) return;
    await http.post(Uri.parse(_url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'title': _controller.text}));
    _controller.clear();
    _fetch();
  }

  Future<void> _update(Todo t, bool done) async {
    await http.put(Uri.parse('$_url${t.id}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'is_done': done}));
    setState(() => t.isDone = done);
  }

  Future<void> _delete(int id) async {
    await http.delete(Uri.parse('$_url$id'));
    setState(() => _todos.removeWhere((x) => x.id == id));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('TODO list')),
      body: ListView.builder(
        itemCount: _todos.length,
        itemBuilder: (c, i) {
          final t = _todos[i];
          return ListTile(
            leading: Checkbox(value: t.isDone, onChanged: (v) => _update(t, v!)),
            title: Text(t.title, style: TextStyle(decoration: t.isDone ? TextDecoration.lineThrough : null)),
            trailing: IconButton(icon: const Icon(Icons.delete), onPressed: () => _delete(t.id)),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => showDialog(
          context: context,
          builder: (_) => AlertDialog(
            title: const Text('Нове завдання'),
            content: TextField(controller: _controller),
            actions: [
              TextButton(onPressed: () => Navigator.pop(context), child: const Text('Скасувати')),
              TextButton(onPressed: () { Navigator.pop(context); _add(); }, child: const Text('Додати')),
            ],
          ),
        ),
        child: const Icon(Icons.add),
      ),
    );
  }
}

// flutter run -d web-server