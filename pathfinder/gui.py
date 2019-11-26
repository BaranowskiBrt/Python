import tkinter as tk
import settings

start = (0, 0)
end = (settings.cols-1, settings.rows-1)

def distance_message(distance):
    master = tk.Tk()
    master.withdraw()
    tk.messagebox.showinfo("Distance", "Calculated distance is equal to {}.".format(distance))

def not_found():
    master = tk.Tk()
    master.withdraw()
    tk.messagebox.showinfo("No path", "There is no path to the destination.")

def start_screen():
    global start, end
    master = tk.Tk()

    tk.Label(master, text="Input coordinates from 0 to 49", font="Courier").grid(row=0, column=1, sticky=tk.N)
    tk.Label(master, text="Start point").grid(row=1)
    tk.Label(master, text="Destination point").grid(row=2)
    startx = tk.Entry(master)
    starty = tk.Entry(master)
    endx = tk.Entry(master)
    endy = tk.Entry(master)

    startx.grid(row=1, column=1)
    starty.grid(row=1, column=2)
    endx.grid(row=2, column=1)
    endy.grid(row=2, column=2)
    var = tk.BooleanVar()

    tk.Checkbutton(master, text="Show steps", variable=var).grid(row=3, column=2, sticky=tk.W)

    def ret(event=None):
        global start, end
        if startx.get() != "" or starty.get() != "" or\
         endx.get() != "" or endy.get() != "":
            start = (int(startx.get()),int(starty.get()))
            end = (int(endx.get()),int(endy.get()))
        settings.steps_on = var.get()
        master.destroy()



    button = tk.Button(master, text="Submit", command=ret).grid(row=4, column=1, sticky=tk.S)
    master.bind('<Return>', ret)


    master.mainloop()
    return (start, end)
