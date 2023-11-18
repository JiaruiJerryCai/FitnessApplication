import 'package:flutter/material.dart';
import 'package:flutter_application/ThirdPage.dart';
import 'package:video_player/video_player.dart';

class SecondPage extends StatefulWidget {
  const SecondPage({super.key, required this.title, required this.info});

  final String title;
  final Map info;


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
    description = widget.info["description"];
    _controller = VideoPlayerController.networkUrl(Uri.parse(widget.info["demo_video"]));
    
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
    Navigator.push(context, MaterialPageRoute(builder: (context) => ThirdPage(title: "Choose a video", exercise: widget.title)));
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
