import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:flutter_application/FourthPage.dart';

class ThirdPage extends StatefulWidget {
  const ThirdPage({super.key, required this.title, required this.exercise});

  final String title;
  final String exercise;


  @override
  State<ThirdPage> createState() => _ThirdPageState();
}

class _ThirdPageState extends State<ThirdPage> {
  // Variable used to store the server response
  late Future<String> server_response; 
  late String videolink;
  File? selectedFile;
  bool enableNextPage = false;

  final picker = ImagePicker();

  void navigateToFourthPage() {
    Navigator.push(context, MaterialPageRoute(builder: (context) => FourthPage(title: "Save Video", videoLink: videolink)));
  }

  // Control what the screen does when it first renders
  @override
  void initState() {
    super.initState();
    server_response = sendRequest('http://3.18.103.214:5000/');
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



      return text;

    } catch (e) {
      print('error caught: $e');
    }

    return "Error connecting to server!";
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

      setState(() {
        videolink = text; // Setting the video link to a variable
        enableNextPage = true;

      });
      navigateToFourthPage();

      return text;

    } catch (e) {
      print('error caught: $e');
    }

    return "Please select a video before analyzing";
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
          server_response = sendExerciseRequest('http://3.18.103.214:5000/exercisevideo');
        } else { 
          ScaffoldMessenger.of(context).showSnackBar(// is this context <<< 
              const SnackBar(content: Text('Nothing is selected'))); 
        } 
      }, 
    ); 
  } 

  Widget nextPageBtn(bool enableNextPage) {
    if(enableNextPage) {
      return ElevatedButton(
        onPressed: navigateToFourthPage,
        child:Text("Go To Save the Edited Video Page"),
      );
    } else {
      return Text("Please select a video");
    }
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
              },
              child:Text("Import Media"),
            ),
            ElevatedButton(
              onPressed: () {
                getVideo(ImageSource.camera);
              },
              child:Text("Start Recording"),
            ),
            serverText(),
          ],
        ),
      ),
    );
  }
}
