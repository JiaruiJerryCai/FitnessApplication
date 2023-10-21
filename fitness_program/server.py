from flask import Flask, request
import json
import fitness_analyzer
import os

app = Flask(__name__)

@app.route("/exercise", methods=['GET', 'POST'])
def showExercise():
    
    chosenExercise = request.form['exercise']
    print(chosenExercise)
    return "You have chosen " + str(chosenExercise)

@app.route("/exercisevideo", methods=['GET', 'POST'])
def analyzeExercise():
    print("Running Route")
    exercise = request.form['exercise']
    print(exercise)
    video = request.files.getlist("exerciseVideo")[0]
    print(video)
    videoname = video.filename # Get the video name from the video
    print(videoname)

    # Downloads the video on to the server
    video.save(videoname)

    # Run analyzer with the downloaded video
    link = fitness_analyzer.fitnessAnalyzer(exercise, videoname, "Analyzed" + exercise)

    # Remove video from server after it is analyzed
    os.remove(videoname)

    return link

if __name__ == '__main__':
    app.run(host='0.0.0.0')