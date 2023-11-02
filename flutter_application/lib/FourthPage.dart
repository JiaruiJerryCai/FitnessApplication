import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:video_player/video_player.dart';
import 'package:flutter_downloader/flutter_downloader.dart';


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
    final taskId = await FlutterDownloader.enqueue(
        url: widget.videoLink,
        headers: {}, // optional: header send with url (auth token etc)
        savedDir: downloadPath,
        showNotification: true, // show download progress in status bar (for Android)
        openFileFromNotification: true, // click on notification to open downloaded file (for Android)
        saveInPublicStorage: true,
      );
  }

  Widget downloadButton() {
    return FutureBuilder<String?> (
      future: downloadPath, 
      builder: (context, snapshot) {
        if(snapshot.hasData) {
          String downloadLocation = snapshot.data as String;
          return ElevatedButton(
            onPressed: () { 
              saveEditedVideo(downloadLocation); 
            }, 
            child: Text('Save Edited Video'),
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
        if (!await directory.exists()) directory = await getExternalStorageDirectory();
      }
    } catch (err, stack) {
      print("Cannot get download folder path");
      print(stack);
    }
    return directory?.path;
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

  Widget playAndPauseBtn() {
    return ElevatedButton(
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
            playAndPauseBtn(),
            downloadButton(),
          ],
        ),
      ),
    );
  }
}
