import 'dart:async';
import 'package:flutter/material.dart';
import 'package:DynamicFit/exercise_page.dart';

class SplashPage extends StatefulWidget {
  const SplashPage({super.key});

  @override
  State<SplashPage> createState() => _SplashPageState();
}

class _SplashPageState extends State<SplashPage> {

  @override
  void initState() {
    super.initState();
    Timer(Duration(milliseconds: 2500), navigateToExercisePage);
  }

  void navigateToExercisePage() {
    Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => ExercisePage()));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center, 
          children: <Widget>[
            Container(
              width: 100, 
              height: 100, 
              child: Image.asset("assets/logo_large_icon_transparent.png"),
            ),
            Text(
              "DynamicFit",
              style: TextStyle(
                fontWeight: FontWeight.bold, 
                fontSize: 25,
                color: Colors.orange,
              ),
            )
          ],
        ),
      ),
    );
  }
}