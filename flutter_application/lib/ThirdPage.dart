import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';

class ThirdPage extends StatefulWidget {
  const ThirdPage({super.key, required this.title});

  final String title;


  @override
  State<ThirdPage> createState() => _ThirdPageState();
}

class _ThirdPageState extends State<ThirdPage> {
  late Future<String> server_response;
  
  Future<String> sendRequest() async {
    try {

      // Define destination link
      Uri link = Uri.parse('http://127.0.0.1:5000');

      // Create request
      http.MultipartRequest request = http.MultipartRequest('GET', link);

      // Send the request and get a response back
      final server_response = await request.send();
      final text = await server_response.stream.bytesToString();
      print(text);
      return text as String;

    } catch (e) {
      print('error caught: $e');
    }

    return "Error caught" as String;
  }

  Widget serverText() {

    return FutureBuilder<String> (
      future: server_response, 
      builder: (context, snapshot) {
        if(snapshot.hasData) {
          String text = snapshot.data as String;
          return Text(text);
        } else {
          return Text("Did not recieve anything");
        }

    });

  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            ElevatedButton(
              onPressed: () { server_response = sendRequest(); } ,
              child:Text("Connect to server"),
            ),
            serverText(),
          ],
        ),
      ),
    );
  }
}
