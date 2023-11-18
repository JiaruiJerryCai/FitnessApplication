from flask import Flask, request, jsonify
import fitness_analyzer
import os
from exercise_table import exerciseTable

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def root():
    return "Connected to server..."

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

    print(link)
    return link

# @app.route("/exerciselist")
# def getExerciseList():
#     exerciseList = ['Pushup', 'Pullup', 'Plank', 'Squat']
#     return jsonify(exerciseList)


@app.route("/exerciseinfo", methods=['GET', 'POST'])
def getExerciseInfo():
    exerciseInfo = exerciseTable
    return jsonify(exerciseInfo)




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)