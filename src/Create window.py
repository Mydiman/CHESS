import tkinter



r = tkinter.Tk()
r.title('Chess')
r.geometry('800x600')

def resign():
    resignWindow = tkinter.Toplevel(r)
    resignWindow.title('Resign')
    resignWindow.geometry('300x60')
    
    def yes():
        resignYes = tkinter.Toplevel(resignWindow)
        resignYes.title('byebye')
        tkinter.Button(resignYes, text='BYEBYE', command=r.destroy).pack()
        resignYes.mainloop()
    
    def no():
        resignWindow.destroy()
    
    label = tkinter.Label(resignWindow, text='Are you sure?', width=42)
    y_button = tkinter.Button(resignWindow, text='Yes', command=yes)
    n_button = tkinter.Button(resignWindow, text='No', command=no)
    label.grid(row=0, column=0, columnspan=2)
    y_button.grid(row=1, column=0)
    n_button.grid(row=1, column=1)
    resignWindow.mainloop()




button = tkinter.Button(r, text='resign', command=resign, activeforeground='red')
button.pack()
r.mainloop()
input("HAHAHA")