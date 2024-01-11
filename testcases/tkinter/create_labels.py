import tkinter as tk
from PIL import Image, ImageTk

# Create our first window
root = tk.Tk()

# Modify and customize the window after it is created and before it is displayed
root.title("My Custom Window") # Defines a title for the window
root.geometry("500x750") # Adjust the size of the window

# ============ Create Label =======================

# Create the label
label1 = tk.Label(root, text="Hello", background="red")
label2 = tk.Label(root, text="Goodbye!", background="blue")


# Display the label
label1.pack()
label2.pack()


# ==================================================

# Display and run the window
root.mainloop()