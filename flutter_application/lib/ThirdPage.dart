import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class ThirdPage extends StatefulWidget {
  const ThirdPage({super.key, required this.title, required this.exercise});

  final String title;
  final String exercise;


  @override
  State<ThirdPage> createState() => _ThirdPageState();
}

class _ThirdPageState extends State<ThirdPage> {
  late Future<String> server_response; // Variable used to store the server response
  File? selectedFile;

  final picker = ImagePicker();



  // Control what the screen does when it first renders
  @override
  void initState() {
    super.initState();
    server_response = sendRequest('http://127.0.0.1:5000/');
  }
  
  // Method used to send a request to the server and return a response value
  Future<String> sendRequest(String url) async {
    try {
      String urlLink = url;
      // Define destination link
      Uri link = Uri.parse(urlLink);

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

  // Method used to send a request to the server and return a response value
  Future<String> sendExerciseRequest(String url) async {
    try {
      String urlLink = url;
      // Define destination link
      Uri link = Uri.parse(urlLink);

      // Create request
      http.MultipartRequest request = http.MultipartRequest('POST', link);

      // Define the headers and add to the request
      Map<String, String> header = {'Content-Type': 'multipart/form-data'};
      request.headers.addAll(header);

      // Fill in the body
      request.fields["exercise"] = widget.exercise;

      // Add video to body of request
      request.files.add(await http.MultipartFile.fromPath("exerciseVideo", selectedFile!.path));

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
  // Custom FutureBuilder Widget
  // Widget used to render the possible values of a Future
  // A result or loading bar
  Widget serverText() {
    return FutureBuilder<String> (
      future: server_response, 
      builder: (context, snapshot) {
        if(snapshot.hasData) {
          String text = snapshot.data as String;
          return Text(text);
        } else {
          return CircularProgressIndicator();
        }

    });

  }

  // The button action to start a recording or select a file from library
  Future getVideo(ImageSource img) async { 
    final pickedFile = await picker.pickVideo( 
        source: img, 
        preferredCameraDevice: CameraDevice.front, 
        maxDuration: const Duration(minutes: 10)); 
    XFile? xfilePick = pickedFile; 
    setState( 
      () { 
        if (xfilePick != null) { 
          selectedFile = File(pickedFile!.path); 
        } else { 
          ScaffoldMessenger.of(context).showSnackBar(// is this context <<< 
              const SnackBar(content: Text('Nothing is selected'))); 
        } 
      }, 
    ); 
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
              onPressed: () {
                getVideo(ImageSource.gallery); 
                print(selectedFile);
              } ,
              child:Text("Import Media"),
            ),
            ElevatedButton(
              onPressed: () {
                getVideo(ImageSource.camera);
              } ,
              child:Text("Start Recording"),
            ),
            ElevatedButton(
              onPressed: () { setState(() { server_response = sendExerciseRequest('http://127.0.0.1:5000/exercisevideo'); }); } ,
              child:Text("Connect to Exercise"),
            ),
            serverText(),
          ],
        ),
      ),
    );
  }
}
