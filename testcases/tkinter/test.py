import tkinter

# Create the window
window = tkinter.Tk()
window.geometry("500x500")

# Counter
global _count
_count = 0

# Create a label widget
myText = tkinter.Label(text = str(_count), bg="green", width=10, height=20)
myText.pack() # Add the label to the window

def increaseCount():
    print("Button clicked!")
    _count = _count + 1

# Create button widget and add to window

myButton = tkinter.Button(text = "Click here!", command=increaseCount)
myButton.pack()


window.mainloop() # Start the window