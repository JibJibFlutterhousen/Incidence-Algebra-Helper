import tkinter

def _do_thing():
    print("Hello World!")

def _make_window(Size):
    window = tkinter.Tk()
    window.title("Child Window")
    tkinter.Label(window, text=Size).grid(row=Size+1)
    GoButton = tkinter.Button(window, text="replicate", command=lambda: _make_window(Size+1)).grid(row=Size+1,column=1)
    Matrixrows = []
    for y in range(1,Size+1,1):
        Matrixcolumns = []
        for x in range(1,Size+1,1):
            if x == y:
                Entry = tkinter.Label(window, text="1")
            elif x > y:
                Entry = tkinter.Label(window, text="")
            else:
                Entry = tkinter.Entry(window)
            Entry.grid(row=x,column=y)
            Matrixcolumns.append(Entry)
        Matrixrows.append(Matrixcolumns)
    window.mainloop()

top = tkinter.Tk()
top.title("Incidence Algebra Creation")
top.geometry("400x250")
# top.state("zoomed")
tkinter.Label(top, text="Matrix size:").grid(row=0)
MatrixDimentions = tkinter.Spinbox(top, from_=4, to=50)
MatrixDimentions.grid(row=0,column=1)
gobutton = tkinter.Button(top, text="calculate", command=lambda: _make_window(int(MatrixDimentions.get()))).grid(row=0,column=2)
top.mainloop()