import sys

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import AMUSEMENT_PARK_SIMULATION_PROJECT as smpj

matplotlib.use('TkAgg')
import tkinter as tk

games = ["Game 1", "Game 2", "Game 3", "Game 4", "Game 5"]


def startSimulation():
    try:
        NOS = int(numOfSim.get())
        NORP = int(numOfRequireprofet.get())
    except:
        print("This is not a number.")
        strval.set("This is not a number.")
    smpj.days.clear()
    smpj.customer_arrival.clear()
    smpj.g = [0, 0, 0, 0, 0]
    # Canvas1.delete("all")
    #  Canvas2.delete("all")
    smpj.startSim(NOS, NORP)
    strval.set("Number of Months %s" % (smpj.months))

    Charts('Number of customers per days', 'Days', 'Number of customers', smpj.days, smpj.customer_arrival, "blue",
           Canvas1)
    Charts('served customers by each game', 'Games', 'Number of served customers', games, smpj.g, "blue", Canvas2)


def Charts(title, xlabel, ylabel, xval, yval, color, Canvas):
    fig = Figure(figsize=(8, 6), dpi=50, tight_layout=True)
    ax = fig.add_subplot(111)
    ax.bar(xval, yval, color='blue')
    ax.set_title(title, fontsize=17)
    ax.set_xlabel(xlabel, fontsize=17)
    ax.set_ylabel(ylabel, fontsize=15)
    canvas = FigureCanvasTkAgg(fig, master=Canvas)
    canvas.get_tk_widget().pack()
    canvas.draw()


def StopSimulation():
    sys.exit()
    sys.stdout.flush()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def start_gui():
    global val, w, root
    root = tk.Tk()
    top = Sim(root)
    init(root, top)
    root.mainloop()


w = None


class Sim:

    # def deleteCan(self, can):
    #   self.canvas.delete(can)

    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'
        _fgcolor = '#000000'
        _compcolor = '#d9d9d9'
        _ana1color = '#d9d9d9'
        _ana2color = '#ececec'

        top.geometry("600x450+383+106")
        top.minsize(120, 1)
        top.maxsize(1370, 749)
        top.resizable(1, 1)
        top.title("Simulation")
        top.configure(background="#fdfdfd")
        top.configure(highlightbackground="#f0f0f0f0f0f0")

        self.Inputs = tk.LabelFrame(top)
        self.Inputs.place(relx=0.017, rely=0.022, relheight=0.344
                          , relwidth=0.967)
        self.Inputs.configure(relief='groove')
        self.Inputs.configure(foreground="black")
        self.Inputs.configure(text='''Inputs''')
        self.Inputs.configure(background="#ffffff")

        global numOfSim, numOfRequireprofet

        numOfSim = tk.Entry(self.Inputs)
        numOfRequireprofet = tk.Entry(self.Inputs)
        self.Text1 = numOfRequireprofet
        self.Text1.place(relx=0.328, rely=0.581, relheight=0.155, relwidth=0.576
                         , bordermode='ignore')
        self.Text1.configure(background="#e6e6e6")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(foreground="black")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(selectbackground="blue")
        self.Text1.configure(selectforeground="white")
        # self.Text1.configure(wrap="word")

        self.TnOfSimulations = numOfSim
        self.TnOfSimulations.place(relx=0.328, rely=0.323, relheight=0.155
                                   , relwidth=0.576, bordermode='ignore')
        self.TnOfSimulations.configure(background="#e6e6e6")
        self.TnOfSimulations.configure(font="TkTextFont")
        self.TnOfSimulations.configure(foreground="black")
        self.TnOfSimulations.configure(highlightbackground="#d9d9d9")
        self.TnOfSimulations.configure(highlightcolor="black")
        self.TnOfSimulations.configure(insertbackground="black")
        self.TnOfSimulations.configure(selectbackground="blue")
        self.TnOfSimulations.configure(selectforeground="white")
        # self.TnOfSimulations.configure(wrap="word")
        # self.TnOfSimulations.configure(textvariable=nOfSimText)

        self.Number_Of_Simulations = tk.Label(self.Inputs)
        self.Number_Of_Simulations.place(relx=0.017, rely=0.355, height=21
                                         , width=154, bordermode='ignore')
        self.Number_Of_Simulations.configure(background="#fbfbfb")
        self.Number_Of_Simulations.configure(disabledforeground="#a3a3a3")
        self.Number_Of_Simulations.configure(foreground="#000000")
        self.Number_Of_Simulations.configure(text='''Number Of Simulations''')

        self.Reruired_Profit = tk.Label(self.Inputs)
        self.Reruired_Profit.place(relx=0.034, rely=0.581, height=21, width=124
                                   , bordermode='ignore')
        self.Reruired_Profit.configure(background="#ffffff")
        self.Reruired_Profit.configure(disabledforeground="#a3a3a3")
        self.Reruired_Profit.configure(foreground="#000000")
        self.Reruired_Profit.configure(text='''Reruired Profit''')

        self.Start = tk.Button(top)
        self.Start.place(relx=0.683, rely=0.382, height=24, width=97)
        self.Start.configure(activebackground="#04e10f")
        self.Start.configure(activeforeground="#ffffff")
        self.Start.configure(background="#e6e6e6")
        self.Start.configure(disabledforeground="#a3a3a3")
        self.Start.configure(foreground="#000000")
        self.Start.configure(command=startSimulation)
        self.Start.configure(highlightbackground="#d9d9d9")
        self.Start.configure(highlightcolor="black")
        self.Start.configure(pady="0")
        self.Start.configure(text='''Start''')

        self.Exit = tk.Button(top)
        self.Exit.place(relx=0.865, rely=0.382, height=24, width=67)
        self.Exit.configure(activebackground="#f20006")
        self.Exit.configure(activeforeground="white")
        self.Exit.configure(activeforeground="#000000")
        self.Exit.configure(background="#e6e6e6")
        self.Exit.configure(disabledforeground="#a3a3a3")
        self.Exit.configure(foreground="#000000")
        self.Exit.configure(highlightbackground="#d9d9d9")
        self.Exit.configure(highlightcolor="black")
        self.Exit.configure(pady="0")
        self.Exit.configure(command=StopSimulation)
        self.Exit.configure(text='''Exit''')

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.017, rely=0.444, relheight=0.544
                               , relwidth=0.967)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''Outputs''')
        self.Labelframe1.configure(background="#ffffff")

        global Canvas1, Canvas2, status, strval
        Canvas1 = tk.Canvas(self.Labelframe1)
        Canvas2 = tk.Canvas(self.Labelframe1)
        status = tk.Label(self.Labelframe1)

        strval = tk.StringVar()
        strval.set("status")

        self.status = status
        self.status.place(relx=0.1, rely=.05, height=15, width=200
                          , bordermode='ignore')
        self.status.configure(background="#ffffff")
        self.status.configure(disabledforeground="#a3a3a3")
        self.status.configure(foreground="#000000")
        self.status.configure(textvariable=strval)

        self.Canvas1 = Canvas1
        self.Canvas1.place(relx=0.534, rely=0.118, relheight=0.747, relwidth=0.4
                           , bordermode='ignore')
        self.Canvas1.configure(background="#d9d9d9")
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(insertbackground="black")
        self.Canvas1.configure(relief="ridge")
        self.Canvas1.configure(selectbackground="blue")
        self.Canvas1.configure(selectforeground="white")

        self.Canvas2 = Canvas2
        self.Canvas2.place(relx=0.053, rely=0.127, relheight=0.747
                           , relwidth=0.383, bordermode='ignore')
        self.Canvas2.configure(background="#d9d9d9")
        self.Canvas2.configure(borderwidth="2")
        self.Canvas2.configure(insertbackground="black")
        self.Canvas2.configure(relief="ridge")
        self.Canvas2.configure(selectbackground="blue")
        self.Canvas2.configure(selectforeground="white")


if __name__ == '__main__':
    start_gui()
