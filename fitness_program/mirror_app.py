import tkinter as tk
import cv2
from PIL import Image, ImageTk
import Exercises.Pullup as Pullup
import Exercises.Pushup as Pushup
import Exercises.Squat as Squat
import Exercises.Plank as Plank
import Exercises.Situp as Situp
import Exercises.Jumpingjacks as Jumpingjacks
import Exercises.Muscleup as Muscleup
import Exercises.Lunge as Lunge
import Exercises.Sideplanks as Sideplanks
import Exercises.Kneeraises as Kneeraises


# Create our first window
root = tk.Tk()

# Modify and customize the window after it is created and before it is displayed
root.title("DynamicFit Mirror") # Defines a title for the window
# root.geometry("600x900") # Adjust the size of the window

# Display an image
# 1) get an image object to handle an img file
# 2) turn the image object into an imageTk
# 3) use either a label or button to display the image

# Image Logo
new_image = Image.open("resources/logo.png")
new_image = new_image.resize((300,300)) # use this line if you need to resize image
new_image = ImageTk.PhotoImage(new_image) # convert image to imagetk
label1 = tk.Label(root, image=new_image) # Created label with image
label1.pack()

# Text "Select your exercise..."
label2 = tk.Label(root, text="Select your exercise...")
label2.pack()

# Button Row using frame
button_frame = tk.Frame(root, background="red")
button_frame.pack()

# Exercises button
pushupLabel = tk.Button(button_frame, text="Pushup", command= lambda: exercise_screen(exercise="Pushup"))
pushupLabel.pack(side=tk.LEFT)

pullupLabel = tk.Button(button_frame, text="Pullup", command= lambda: exercise_screen(exercise="Pullup"))
pullupLabel.pack(side=tk.LEFT)

squatLabel = tk.Button(button_frame, text="Squat", command= lambda: exercise_screen(exercise="Squat"))
squatLabel.pack(side=tk.LEFT)

plankLabel = tk.Button(button_frame, text="Plank", command= lambda: exercise_screen(exercise="Plank"))
plankLabel.pack(side=tk.LEFT)

situpLabel = tk.Button(button_frame, text="Sit Up", command= lambda: exercise_screen(exercise="Sit Up"))
situpLabel.pack(side=tk.LEFT)

jumpingjacksLabel = tk.Button(button_frame, text="Jumping Jacks", command= lambda: exercise_screen(exercise="Jumping Jacks"))
jumpingjacksLabel.pack(side=tk.LEFT)

muscleupLabel = tk.Button(button_frame, text="Muscle Up", command= lambda: exercise_screen(exercise="Muscle Up"))
muscleupLabel.pack(side=tk.LEFT)

lungeLabel = tk.Button(button_frame, text="Lunge", command= lambda: exercise_screen(exercise="Lunge"))
lungeLabel.pack(side=tk.LEFT)

sideplankLabel = tk.Button(button_frame, text="Side Plank", command= lambda: exercise_screen(exercise="Side Plank"))
sideplankLabel.pack(side=tk.LEFT)

kneeraiseLabel = tk.Button(button_frame, text="Knee Raise", command= lambda: exercise_screen(exercise="Knee Raise"))
kneeraiseLabel.pack(side=tk.LEFT)


def exercise_screen(exercise):

    # Exercise window
    screen = tk.Toplevel() # Create window
    screen.title(str(exercise + " Analyzer")) # Customize window
    screen.geometry("600x800") # Display window

    # Webcam Display
    webcam_canvas = tk.Canvas(screen, width=640, height=480, background="purple") # Create widget
    webcam_canvas.pack()    # Display canvas

    # Go Back button
    goBack = tk.Button(screen, text="Go Back To Home Page", command= lambda: go_back(screen=screen, webcam=webcam))
    goBack.pack()

    # Accessing the webcam using opencv2
    webcam = cv2.VideoCapture(0)
    fps = webcam.get(cv2.CAP_PROP_FPS)

    # Define the analyzer
    analyzer = None
    if exercise == 'Pushup':
        analyzer = Pushup.set()
        print("Running Pushup")
    if exercise == 'Pullup':
        analyzer = Pullup.set()
        print("Running Pullup")
    if exercise == 'Squat':
        analyzer = Squat.set()
        print('Running Squat')
    if exercise == 'Plank':
        analyzer = Plank.set(fps)
        print("Running Plank")
    if exercise == 'Sit Up':
        analyzer = Situp.set()
        print("Running Sit Up")
    if exercise == "Jumping Jacks":
        analyzer = Jumpingjacks.set()
        print("Running Jumping Jack")
    if exercise == "Muscle Up":
        analyzer = Muscleup.set()
        print("Running Muscle Up")
    if exercise == "Lunge":
        analyzer = Lunge.set()
        print("Running Lunge")
    if exercise == "Side Plank":
        analyzer = Sideplanks.set(fps)
        print("Running Side Planks")
    if exercise == "Knee Raise":
        analyzer = Kneeraises.set()
        print("Running Knee Raise")

    def update():
        success, frame = webcam.read()
        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            analyzer.process(frame)
            frame = cv2.resize(frame, (640, 480))

            webcam_frame = ImageTk.PhotoImage(image=Image.fromarray(frame, mode='RGB'))
            webcam_canvas.create_image(0, 0, image=webcam_frame, anchor=tk.NW)
            webcam_canvas.photo = webcam_frame
        screen.after(10, update)

    update()
    screen.mainloop()

def go_back(screen, webcam):
    screen.destroy()
    webcam.release()


# Display and run the window
root.mainloop()