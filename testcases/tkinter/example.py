import tkinter
from PIL import Image, ImageTk

# Create the window
window = tkinter.Tk()
window.geometry("500x500")
# window.config(background="white")

myCanvas = tkinter.Canvas(bd=2, highlightthickness=2, bg="black")
myCanvas.pack()

# Using images

# Open images using Image in PIL
newImage = Image.open("resources/bp.png")
resizedImage = newImage.resize((300,300)) # resize images using PIL
myImage = ImageTk.PhotoImage(resizedImage)  # create tkinter image

# Create label
myLabel = tkinter.Label(myCanvas, text="0")
myLabel.pack()

def increaseCounter():
    global count
    count = count + 1
    myLabel.config(text=str(count))

count = 0



myButton = tkinter.Button(myCanvas, command= lambda: increaseCounter(), image=myImage, bg="black", fg="black", highlightbackground="black", highlightcolor="black", bd=0, borderwidth=0)  # give image to button
myButton.pack()

window.mainloop() # Start the window
