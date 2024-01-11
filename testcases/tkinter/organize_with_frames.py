import tkinter as tk
from PIL import Image, ImageTk

# Create our first window
root = tk.Tk()

# Modify and customize the window after it is created and before it is displayed
root.title("My Custom Window") # Defines a title for the window
root.geometry("500x750") # Adjust the size of the window

# Create frames to act as rows for the labels
frame1 = tk.Frame(root, background="green")
frame2 = tk.Frame(root, background="white")

frame1.pack()
frame2.pack()

# Create the label
label1 = tk.Label(frame1, text="Hello", background="red")
label2 = tk.Label(frame1, text="Goodbye!", background="blue")
label3 = tk.Label(frame1, text="left1", background="purple")
label4 = tk.Label(frame1, text="left2", background="cyan")

label5 = tk.Label(frame2, text="Hello", background="red")
label6 = tk.Label(frame2, text="Goodbye!", background="blue")
label7 = tk.Label(frame2, text="left1", background="purple")
label8 = tk.Label(frame2, text="left2", background="cyan")

# Display the label
label1.pack(side=tk.LEFT)
label2.pack(side=tk.LEFT)
label3.pack(side=tk.LEFT)
label4.pack(side=tk.LEFT)

label5.pack()
label6.pack()
label7.pack()
label8.pack()

# Display and run the window
root.mainloop()