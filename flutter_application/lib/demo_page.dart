import 'package:flutter/material.dart';
import 'package:flutter_application/submit_video_page.dart';
import 'package:video_player/video_player.dart';

class DemoPage extends StatefulWidget {
  const DemoPage({super.key, required this.title, required this.info});

  final String title;
  final Map info;

  @override
  State<DemoPage> createState() => _DemoPageState();
}

class _DemoPageState extends State<DemoPage> {
  late VideoPlayerController _controller;
  late Future<void> _initializeVideoPlayerFuture;

  @override
  void initState() {
    super.initState();

    // Create and store the VideoPlayerController. The VideoPlayerController
    // offers several different constructors to play videos from assets, files,
    // or the internet.
    _controller =
        VideoPlayerController.networkUrl(Uri.parse(widget.info["demo_video"]));
    _initializeVideoPlayerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    // Ensure disposing of the VideoPlayerController to free up resources.
    _controller.dispose();
    super.dispose();
  }

  // Use a FutureBuilder to display a loading spinner while waiting for the
  // VideoPlayerController to finish initializing.
  Widget ExerciseVideo() {
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

  void navigateToSubmitVideoPage() {
    Navigator.push(
        context,
        MaterialPageRoute(
            builder: (context) => SubmitVideoPage(
                title: "Choose a video", exercise: widget.title)));
  }

  Widget DescriptionBanner() {
    return Container(
      width: double.infinity,
      margin: EdgeInsets.all(10.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.all(Radius.circular(25.0)),
        image: DecorationImage(
          image: NetworkImage(widget.info["image"]),
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
              Colors.black.withOpacity(0.5),
            ],
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: 300,
                  padding: EdgeInsets.symmetric(vertical: 10.0),
                  child: Text(
                    widget.info["description"],
                    style: TextStyle(
                      color: Colors.white,
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

  Widget DemoVideo() {
    return Container(
      color: Colors.orange,
      child: Column(
        children: <Widget>[
          Padding(
            padding: const EdgeInsets.only(top: 8.0),
            child: Text(
              "Demonstration Video",
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.w300,
                fontSize: 15.0,
              ),
            ),
          ),
          Container(
            margin: EdgeInsets.all(10.0),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.all(Radius.circular(25.0)),
            ),
            child: ExerciseVideo(),
          ),
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
          SizedBox(height: 10.0),
        ],
      ),
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
            child: ElevatedButton(
              onPressed: navigateToSubmitVideoPage,
              style: ButtonStyle(
                backgroundColor: MaterialStateProperty.all(
                    Colors.black), // Background color of the button
                foregroundColor: MaterialStateProperty.all(
                    Colors.white), // Text color of the button
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Padding(
                    padding: const EdgeInsets.only(right: 8.0),
                    child: Text(
                      'Start Workout!',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 12.0,
                      ),
                    ),
                  ),
                  Icon(Icons.arrow_forward_ios),
                ],
              ),
            ),
          ),
        ],
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
        child: ListView(
          children: <Widget>[
            DescriptionBanner(),
            SizedBox(height: 20.0),
            DemoVideo(),
            SizedBox(height: 20.0),
            NavigationRow(),
          ],
        ),
      ),
    );
  }
}
