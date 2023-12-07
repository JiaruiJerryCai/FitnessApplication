import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:flutter_application/result_page.dart';

class SubmitVideoPage extends StatefulWidget {
  const SubmitVideoPage(
      {super.key, required this.title, required this.exercise});

  final String title;
  final String exercise;

  @override
  State<SubmitVideoPage> createState() => _SubmitVideoPageState();
}

class _SubmitVideoPageState extends State<SubmitVideoPage> {
  // Variable used to store the server response
  late Future<String> server_response;
  late String videolink;
  File? selectedFile;
  bool enableNextPage = false;

  final picker = ImagePicker();

  void navigateToFourthPage() {
    Navigator.push(
        context,
        MaterialPageRoute(
            builder: (context) =>
                ResultPage(title: "Save Video", videoLink: videolink)));
  }

  // Control what the screen does when it first renders
  @override
  void initState() {
    super.initState();
    server_response = sendRequest('http://localhost:5000/'); // http://3.18.103.214:5000/
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
      request.files.add(await http.MultipartFile.fromPath(
          "exerciseVideo", selectedFile!.path));

      // Send the request and get a response back
      final server_response = await request.send();
      final text = await server_response.stream.bytesToString();
      print("This is the video link");
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
    return FutureBuilder<String>(
        future: server_response,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
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
          server_response =
              sendExerciseRequest('http://localhost:5000/exercisevideo'); // http://3.18.103.214:5000/exercisevideo
        } else {
          ScaffoldMessenger.of(context).showSnackBar(// is this context <<<
              const SnackBar(content: Text('Nothing is selected')));
        }
      },
    );
  }

  Widget NavigationRow() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: <Widget>[
          Expanded(
            child: ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: <Widget>[
                  Icon(Icons.arrow_back_ios),
                  Text(
                    'Select Exercise!',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 12.0,
                    ),
                  ),
                ],
              ),
            ),
          ),
          SizedBox(width: 30.0),
          Expanded(
            child: Container(),
          ),
        ],
      ),
    );
  }

  Widget GalleryButton() {
    return Container(
      height: 150,
      width: 150,
      child: ElevatedButton(
        style: ButtonStyle(
          shape: MaterialStateProperty.all<RoundedRectangleBorder>(
            RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(
                  10.0), // Adjust the value to control the roundness
            ),
          ),
          padding: MaterialStateProperty.all<EdgeInsetsGeometry>(
              EdgeInsets.all(16.0)),
          backgroundColor: MaterialStateProperty.all<Color>(Colors.black),
          foregroundColor: MaterialStateProperty.all<Color>(Colors.white),
        ),
        onPressed: () {
          print("sent video to server from gallery");
          getVideo(ImageSource.gallery);
        },
        child: Text(
          "Import Media from Gallery",
          textAlign: TextAlign.center,
        ),
      ),
    );
  }

  Widget CameraButton() {
    return Container(
      height: 150,
      width: 150,
      child: ElevatedButton(
        style: ButtonStyle(
          shape: MaterialStateProperty.all<RoundedRectangleBorder>(
            RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(
                  10.0), // Adjust the value to control the roundness
            ),
          ),
          padding: MaterialStateProperty.all<EdgeInsetsGeometry>(
              EdgeInsets.all(16.0)),
          backgroundColor: MaterialStateProperty.all<Color>(Colors.black),
          foregroundColor: MaterialStateProperty.all<Color>(Colors.white),
        ),
        onPressed: () {
          getVideo(ImageSource.camera);
        },
        child: Text(
          "Import Media from Camera",
          textAlign: TextAlign.center,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: false,
        titleSpacing: 0.0,
        leading: Image.asset("assets/logo_large_icon_transparent.png"),
        title: Text(
          widget.title,
          textAlign: TextAlign.left,
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 25,
            color: Colors.orange,
          ),
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            SizedBox(height: 100.0),
            GalleryButton(),
            SizedBox(height: 40.0),
            CameraButton(),
            SizedBox(height: 40.0),
            serverText(),
            SizedBox(height: 40.0),
            NavigationRow(),
          ],
        ),
      ),
    );
  }
}
