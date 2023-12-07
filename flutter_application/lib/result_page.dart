import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:video_player/video_player.dart';
import 'package:flutter_downloader/flutter_downloader.dart';

class ResultPage extends StatefulWidget {
  const ResultPage({super.key, required this.title, required this.videoLink});

  final String title;
  final String videoLink;

  @override
  State<ResultPage> createState() => _ResultPageState();
}

class _ResultPageState extends State<ResultPage> {
  // Variables to control the video player
  late VideoPlayerController _controller;
  late Future<void> _initializeVideoPlayerFuture;

  late Future<String?> downloadPath;

  // Control what the screen does when it first renders
  @override
  void initState() {
    super.initState();

    downloadPath = getDownloadPath();

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

  void saveEditedVideo(String downloadPath) async {
    await FlutterDownloader.enqueue(
      url: widget.videoLink,
      headers: {}, // optional: header send with url (auth token etc)
      savedDir: downloadPath,
      showNotification:
          true, // show download progress in status bar (for Android)
      openFileFromNotification:
          true, // click on notification to open downloaded file (for Android)
      saveInPublicStorage: true,
    );
  }

  Widget DownloadButton() {
    return FutureBuilder<String?>(
        future: downloadPath,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            String downloadLocation = snapshot.data as String;

            return Expanded(
              child: ElevatedButton(
                onPressed: () {
                  saveEditedVideo(downloadLocation);
                },
                style: ButtonStyle(
                  backgroundColor: MaterialStateProperty.all(
                      Colors.black), // Background color of the button
                  foregroundColor: MaterialStateProperty.all(
                      Colors.white), // Text color of the button
                ),
                child: Text(
                  'Save Video!',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 12.0,
                  ),
                ),
              ),
            );
          } else {
            return CircularProgressIndicator();
          }
        });
  }

  Future<String?> getDownloadPath() async {
    Directory? directory;
    try {
      if (Platform.isIOS) {
        directory = await getApplicationDocumentsDirectory();
      } else {
        directory = Directory('/storage/emulated/0/Download');
        // Put file in global download folder, if for an unknown reason it didn't exist, we fallback
        // ignore: avoid_slow_async_io
        if (!await directory.exists())
          directory = await getExternalStorageDirectory();
      }
    } catch (err, stack) {
      print("Cannot get download folder path");
      print(stack);
    }
    print(directory?.path);
    return directory?.path;
  }

  Widget AnalyzedVideo() {
    return Container(
      color: Colors.orange,
      child: Column(
        children: <Widget>[
          Padding(
            padding: const EdgeInsets.only(top: 8.0),
            child: Text(
              "Analyzed Video",
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
                    'Select Video!',
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
          DownloadButton(),
        ],
      ),
    );
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
            SizedBox(height: 100),
            AnalyzedVideo(),
            SizedBox(height: 100),
            NavigationRow(),
          ],
        ),
      ),
    );
  }
}
