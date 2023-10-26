import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';


class FourthPage extends StatefulWidget {
  const FourthPage({super.key, required this.title, required this.videoLink});

  final String title;
  final String videoLink;


  @override
  State<FourthPage> createState() => _FourthPageState();
}

class _FourthPageState extends State<FourthPage> {

  // Variables to control the video player
  late VideoPlayerController _controller;
  late Future<void> _initializeVideoPlayerFuture;

  // Control what the screen does when it first renders
  @override
  void initState() {
    super.initState();
    
    // Set up the video variables
    _controller = VideoPlayerController.networkUrl(Uri.parse(widget.videoLink));
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
  
  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            Text('Edited Video'),
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
            ),
            ElevatedButton(
              onPressed: null,
              child: Text("Save Edited Video"),
            )
          ],
        ),
      ),
    );
  }
}
