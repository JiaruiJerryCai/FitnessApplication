import 'package:flutter/material.dart';
import 'package:flutter_application/ThirdPage.dart';
import 'package:video_player/video_player.dart';

class SecondPage extends StatefulWidget {
  const SecondPage({super.key, required this.title});

  final String title;


  @override
  State<SecondPage> createState() => _SecondPageState();
}

class _SecondPageState extends State<SecondPage> {
  late VideoPlayerController _controller;
  late Future<void> _initializeVideoPlayerFuture;

  late String description;

  @override
  void initState() {
    super.initState();

    // Create and store the VideoPlayerController. The VideoPlayerController
    // offers several different constructors to play videos from assets, files,
    // or the internet.

    if (widget.title == "Pushup") {
      description = "\t Pushups are calisthenic exercises that primarily targets the muscles of the chest, shoulders, and triceps. The exercise involves the individual lying prone on the ground, placing their hands slightly wider than shoulder-width apart, and then pushing their body up and down using the arms. The core muscles also play a role in stabilizing the body during the movement. Push-ups are a versatile and effective bodyweight exercise that can be adapted to different fitness levels and variations to target various muscle groups. They are commonly included in fitness routines to improve upper body strength and endurance.";
      _controller = VideoPlayerController.asset('assets/pushup.mp4');
    } else if (widget.title == "Pullup") {
      description = "\t Pullups are strength training exercises that target the muscles of the upper body, particularly the back, shoulders, and arms. The exercise involves suspending oneself from a horizontal bar using an overhand grip (palms facing away from the body) with hands placed slightly wider than shoulder-width apart. The individual then pulls their body upward by bending their arms at the elbows until the chin reaches or clears the bar. Pull-ups primarily engage the latissimus dorsi (lats) muscles, as well as the biceps, rhomboids, and various muscles in the upper back. \n \t Pull-ups are considered a challenging bodyweight exercise, requiring upper body strength and control. They can be performed with different grip variations, such as wide grip, narrow grip, or underhand (chin-up), to target various muscle groups. Pull-ups are commonly incorporated into strength training and calisthenics routines to enhance overall upper body strength and muscular development.";
      _controller = VideoPlayerController.asset('assets/pullup.mp4');
    } else if (widget.title == "Squat") {
      description = "\t Squat are compound exercises that target multiple muscle groups, including the quadriceps, hamstrings, glutes, and muscles in the lower back. It is a fundamental movement pattern that involves bending the knees and hips while keeping the back straight, typically with a downward and upward motion.";
      _controller = VideoPlayerController.asset('assets/squat.mp4');
    } else if (widget.title == "Plank") {
      description = "\t Planks are core-strengthening exercises that involve maintaining a static position, typically in a straight line from head to heels. It is an isometric exercise, meaning the muscles are contracted without any joint movement. \n \t Planks primarily target the core muscles, including the rectus abdominis, transverse abdominis, and obliques.";
      _controller = VideoPlayerController.asset('assets/plank.mp4');
    }
    
    _initializeVideoPlayerFuture = _controller.initialize();

  }

  @override
  void dispose() {
    // Ensure disposing of the VideoPlayerController to free up resources.
    _controller.dispose();

    super.dispose();
  
}

Widget videoDemo() {
  return FutureBuilder(
    future: _initializeVideoPlayerFuture,
    builder: (context, snapshot) {
      if (snapshot.connectionState == ConnectionState.done) {
        // If the VideoPlayerController has finished initialization, use
        // the data it provides to limit the aspect ratio of the video.
        return AspectRatio(
          aspectRatio: _controller.value.aspectRatio,
          // Use the VideoPlayer widget to display the video.
          child: VideoPlayer(_controller),
        );
      } else {
        // If the VideoPlayerController is still initializing, show a
        // loading spinner.
        return const Center(
          child: CircularProgressIndicator(),
        );
      }
    },
  );
}
// Use a FutureBuilder to display a loading spinner while waiting for the
// VideoPlayerController to finish initializing.
  
  void navigateToThirdPage() {
    Navigator.push(context, MaterialPageRoute(builder: (context) => ThirdPage(title: "Camera", exercise: widget.title)));
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: ListView(
          children: <Widget>[
            Container(
              height: 200,
              child: Text(description),
            ),
            Divider(
              height: 20,
              thickness: 3,
              color: Colors.black,
            ),
            Container(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                children: <Widget>[
                  Text('Correct Move Demonstration'),
                  videoDemo(),
                  ElevatedButton(
                    onPressed: () {
                      // Wrap the play or pause in a call to `setState`. This ensures the
                      // correct icon is shown.
                      setState(() {
                        // If the video is playing, pause it.
                        if (_controller.value.isPlaying) {
                          _controller.pause();
                        } else {
                          // If the video is paused, play it.
                          _controller.play();
                        }
                      });
                    },
                    child: Icon(
                      _controller.value.isPlaying ? Icons.pause : Icons.play_arrow,
                    ),
                  )
                ]
              ),
            ),
            Divider(
              height: 20,
              thickness: 3,
              color: Colors.black,
            ),
            UnconstrainedBox(
              child: Container(
                height: 100,
                width: 300,
                child: ElevatedButton(
                  onPressed: navigateToThirdPage,
                  child: Text('Start Workout!'),
                ),
              ),
            )
          ]
        ),
      ),
    );
  }
}
