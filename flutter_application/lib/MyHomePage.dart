import 'package:flutter/material.dart';
import 'package:flutter_application/SecondPage.dart';
import 'package:http/http.dart' as http;


class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  late Future<List> server_response; 

  // Control what the screen does when it first renders
  @override
  void initState() {
    super.initState();
    
    server_response = sendRequest('http://127.0.0.1:5000/exerciselist');
  }

  void navigateToSecondPage(String exercise) {
    Navigator.push(context, MaterialPageRoute(builder: (context) => SecondPage(title: exercise)));
  }

  // Method used to send a request to the server and return a response value
  Future<List> sendRequest(String url) async {
    try {
      String urlLink = url;
      // Define destination link
      Uri link = Uri.parse(urlLink);

      // Create request
      http.MultipartRequest request = http.MultipartRequest('GET', link);

      // Send the request and get a response back
      final server_response = await request.send();
      final response_data = await server_response.stream.bytesToString();
      
      List exercises = stringToList(response_data);
      return exercises;

    } catch (e) {
      print('error caught: $e');
    }

    return [];
  }

  List stringToList(String text) {
    List myList = [];

    // Split the string by ',' and return the elements in a list
    List splitList = text.split(',');
    for (int i = 0; i < splitList.length; i++) {
      String myWord = splitList[i];
      int start = myWord.indexOf('"') + 1;
      int end = myWord.lastIndexOf('"');
      myWord = myWord.substring(start, end);
      myList.add(myWord);
    }

    return myList;
  }


  Widget ExerciseListView() {
    return FutureBuilder<List> (
      future: server_response, 
      builder: (context, snapshot) {
        if(snapshot.hasData) {
          List exercises = snapshot.data as List;

          List<Widget> exerciseRows = [];
          for (int i = 0; i < exercises.length; i++) {
            if (i % 2 == 0) {
              exercises.add(
                  customRow("assets/"+exercises[i]+".jpeg", "start", exercises[i]));
            } else {
              exercises.add(
                  customRow("assets/"+exercises[i]+".jpeg", "end", exercises[i]));
            }
          }
          return ListView(children: exerciseRows);
        } else {
          return Text("Unable to get exercises from server...");
        }

    });

  }

  Widget customRow(String imageLocation, String position, String text) {
      if(position == "start") {
        return Row(
                mainAxisAlignment: MainAxisAlignment.start, // effected by position
                children: <Widget>[
                  Container(
                    margin: const EdgeInsets.all(25),
                    width: 200,
                    height: 200,
                    child: ElevatedButton(
                      onPressed: () { navigateToSecondPage(text); },
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                          ClipRRect(
                            borderRadius: BorderRadius.circular(24),
                            child: Image(
                            image: AssetImage(imageLocation) // image will be based on argument
                            ),
                          ),
                          Text(text)
                        ]
                      )
                    ),
                  ),
                ],
              );
      } else {
          return Row(
                mainAxisAlignment: MainAxisAlignment.end, // effected by position
                children: <Widget>[
                  Container(
                    margin: const EdgeInsets.all(25),
                    width: 200,
                    height: 200,
                    child: ElevatedButton(
                      onPressed: () { navigateToSecondPage(text); },
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                          ClipRRect(
                            borderRadius: BorderRadius.circular(24),
                            child: Image(
                            image: AssetImage(imageLocation) // image will be based on argument
                            ),
                          ),
                          Text(text)
                        ]
                      )
                    ),
                  ),
                ],
              );
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
        child: SizedBox(
          width: 700,
          child: ExerciseListView(),
        )
      ),
    );
  }
}
