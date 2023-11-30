import 'dart:convert';
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
  late Future<Map> server_response; 

  // Control what the screen does when it first renders
  @override
  void initState() {
    super.initState();
    
    server_response = sendRequest('http://3.18.103.214:5000/exerciseinfo');
  }

  void navigateToSecondPage(String exercise, Map exerciseObj) {
    Navigator.push(context, MaterialPageRoute(builder: (context) => SecondPage(title: exercise, info: exerciseObj)));
  }

  // Method used to send a request to the server and return a response value
  Future<Map> sendRequest(String url) async {
    try {
      String urlLink = url;
      // Define destination link
      Uri link = Uri.parse(urlLink);

      // Send the request and get a response back
      final server_response = await http.get(link);

      final Map<String, dynamic> exerciseInfo = jsonDecode(server_response.body);
      // print("Map: ");
      // print(exerciseInfo);
      
      // final List<String> exercises = exerciseInfo.keys.toList();
      // print("Exercises in Map: ");
      // print(exercises);
      
      // for(int i=0; i<exercises.length; i++) {
      //   print("Key: " + exercises[i]);
      //   print("value: ");
      //   print(exerciseInfo[exercises[i]]);
      //   print(exerciseInfo[exercises[i]]["image"]);
      //   print(exerciseInfo[exercises[i]]["demo_video"]);
      //   print(exerciseInfo[exercises[i]]["description"]);
      // }


      return exerciseInfo;

    } catch (e) {
      print('error caught: $e');
    }

    return {};
  }


  Widget ExerciseListView() {
    return FutureBuilder<Map> (
      future: server_response, 
      builder: (context, snapshot) {
        if(snapshot.hasData) {
          Map exerciseInfo = snapshot.data as Map;

          final List exercises = exerciseInfo.keys.toList();

          List<Widget> exerciseRows = [];
          for (int i = 0; i < exercises.length; i++) {
            if (i % 2 == 0) {
              exerciseRows.add(
                  customRow(exerciseInfo[exercises[i]], "start", exercises[i]));
            } else {
              exerciseRows.add(
                  customRow(exerciseInfo[exercises[i]], "end", exercises[i]));
            }
          }
          return ListView(children: exerciseRows);
        } else {
          return Text("Unable to get exercises from server...");
        }
    });
  }

  Widget customRow(Map exerciseObj, String position, String exerciseName) {
      if(position == "start") {
        return Row(
                mainAxisAlignment: MainAxisAlignment.start, // effected by position
                children: <Widget>[
                  Container(
                    margin: const EdgeInsets.all(25),
                    width: 200,
                    height: 200,
                    child: ElevatedButton(
                      onPressed: () { navigateToSecondPage(exerciseName, exerciseObj); },
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                          ClipRRect(
                            borderRadius: BorderRadius.circular(24),
                            child: Image(
                            image: NetworkImage(exerciseObj["image"]) // image will be based on argument
                            ),
                          ),
                          Text(exerciseName)
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
                      onPressed: () { navigateToSecondPage(exerciseName, exerciseObj); },
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                          ClipRRect(
                            borderRadius: BorderRadius.circular(24),
                            child: Image(
                            image: NetworkImage(exerciseObj["image"]) // image will be based on argument
                            ),
                          ),
                          Text(exerciseName)
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
