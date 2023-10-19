import 'package:flutter/material.dart';
import 'package:flutter_application/SecondPage.dart';


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
  final double spacing = 25;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  void navigateToSecondPage() {
    Navigator.push(context, MaterialPageRoute(builder: (context) => SecondPage(title: "Pushup")));
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
                      onPressed: navigateToSecondPage,
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
                      onPressed: navigateToSecondPage,
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
          child: ListView(
            children: <Widget>[
              customRow("assets/pushup.webp","start","Pushup"),
              customRow("assets/pushup.webp","end","Pushup"),
              customRow("assets/pushup.webp","start","Pushup"),
              customRow("assets/pushup.webp","end","Pushup"),
            ],
          ),
        )
      ),
    );
  }
}
