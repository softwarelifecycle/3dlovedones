import tkinter as tk
root = tk.Tk()

root.geometry("1800x700")  

myLabel = tk.Label(root, text="3D Loved Ones")
myLabel.pack()

button = tk.Button(root, text="Take Picture!", height=2, width=50, bg="blue", fg="white")
button.pack()

root.mainloop()

