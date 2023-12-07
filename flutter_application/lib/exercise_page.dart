import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_application/demo_page.dart';
import 'package:http/http.dart' as http;
import 'package:carousel_slider/carousel_slider.dart';

class ExercisePage extends StatefulWidget {
  const ExercisePage({super.key});

  @override
  State<ExercisePage> createState() => _ExercisePageState();
}

class _ExercisePageState extends State<ExercisePage> {
  late Future<Map> server_response;

  // Control what the screen does when it first renders
  @override
  void initState() {
    super.initState();

    server_response = sendRequest('http://localhost:5000/exerciseinfo'); // 'http://3.18.103.214:5000/exerciseinfo'
  }

  void navigateToDemoPage(String exercise, Map exerciseObj) {
    Navigator.push(
        context,
        MaterialPageRoute(
            builder: (context) =>
                DemoPage(title: exercise, info: exerciseObj)));
  }

  // Method used to send a request to the server and return a response value
  Future<Map> sendRequest(String url) async {
    try {
      String urlLink = url;
      // Define destination link
      Uri link = Uri.parse(urlLink);

      // Send the request and get a response back
      final server_response = await http.get(link);

      final Map<String, dynamic> exerciseInfo =
          jsonDecode(server_response.body);

      return exerciseInfo;
    } catch (e) {
      print('error caught: $e');
    }

    return {};
  }

  // The carousel for the list of available exercises
  Widget ExerciseCarousel() {
    return FutureBuilder<Map>(
      future: server_response,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          Map exerciseInfo = snapshot.data as Map;

          final List exercises = exerciseInfo.keys.toList();
          List<Widget> exerciseCards = [];
          for (int i = 0; i < exercises.length; i++) {
            exerciseCards
                .add(customCard(exerciseInfo[exercises[i]], exercises[i]));
          }

          return customCarousel(exerciseCards);
        } else {
          return Text("Unable to get exercises from server...");
        }
      },
    );
  }

  // A template carousel used to scroll through a list of cards
  // Controls the settings of the carousel
  Widget customCarousel(List<Widget> cardList) {
    return Container(
      child: CarouselSlider(
        options: CarouselOptions(
          autoPlay: false,
          aspectRatio: 2.0,
          enlargeCenterPage: true,
        ),
        items: cardList,
      ),
    );
  }

  // Builds the image with text on top
  // Controls the size and formatting of the image
  // image function is controlled here as well
  Widget customCard(Map exerciseObj, String exerciseName) {
    return Container(
      child: Container(
        margin: EdgeInsets.all(5.0),
        child: ClipRRect(
          borderRadius: BorderRadius.all(Radius.circular(5.0)),
          child: GestureDetector(
            onTap: () {
              navigateToDemoPage(exerciseName, exerciseObj);
            },
            child: Stack(
              children: [
                // Image
                ClipRRect(
                  borderRadius: BorderRadius.circular(30),
                  child: Image.network(
                    exerciseObj["image"],
                    fit: BoxFit.cover,
                    width: 300.0,
                    height: 300.0,
                  ),
                ),
                // Positioned text at the bottom left corner
                Positioned(
                  bottom: 8.0, // Adjust the bottom padding
                  left: 15.0, // Adjust the left padding
                  child: Text(
                    exerciseName,
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 20.0,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget PageBanner() {
    return Container(
      height: 250,
      width: double.infinity,
      margin: EdgeInsets.all(10.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.all(Radius.circular(25.0)),
        image: DecorationImage(
          image: AssetImage("assets/page_banner.png"),
          fit: BoxFit.cover,
        ),
      ),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.all(Radius.circular(25.0)),
          gradient: LinearGradient(
            begin: Alignment.bottomRight,
            colors: [
              Colors.black.withOpacity(0.8),
              Colors.black.withOpacity(0.2),
            ],
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.end,
          children: <Widget>[
            Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Padding(
                  padding: EdgeInsets.only(left: 20.0, bottom: 20.0),
                  child: Text(
                    "Welcome!",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 30.0,
                      fontWeight: FontWeight.w300,
                    ),
                  ),
                ),
              ],
            ),
          ],
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
          "DynamicFit",
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
            PageBanner(),
            SizedBox(height: 20.0),
            Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.only(left: 10.0),
                  child: Text(
                    "Exercises",
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 20.0,
                    ),
                  ),
                ),
              ],
            ),
            ExerciseCarousel(),
          ],
        ),
      ),
    );
  }
}
