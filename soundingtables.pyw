# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a sounding table program

This program uses .csv files in the format 
"Trim",value,value,... 
Sounding,contents,contents... 
Sounding,contents,contents... 

files named as Tank.csv in ./soundingtables/

Created by Joseph Douce
"""
import tkinter
from tkinter import ttk
from tkinter import messagebox
import glob

#set bg colour 
bg = "lightblue"

#setup mainwindow
mainwindow = tkinter.Tk()
mainwindow.title("Sounding Tables")
mainwindow["bg"] =  bg

#define ttk styles for widgets 
style = ttk.Style()
style.configure("TButton", padding=5, background=bg)
style.configure("TFrame", background=bg)
style.configure("TEntry", background=bg)
style.configure("TLabel", background=bg)
style.configure("TScale", background=bg)

#global widget varibales
soundingset = tkinter.StringVar()
tankset = tkinter.StringVar()
trimset = tkinter.StringVar()
displayset = tkinter.StringVar()

#global variables
soundingtable = {}
trimtable = {}

#import list of tanks from folder /soundingtables/
tanks = glob.glob('./soundingtables/*.csv')

#slice the path and .csv fom the tank names        
def slicetanks():
    i=0
    for tank in tanks:
        tanks[i] = tanks[i][17:-4]
        i=i+1
        
slicetanks()

#make the widgets
def makewidgets():    
#tank select combobox & label
    
    tanklabel = ttk.Label(mainwindow)
    tanklabel["text"] = "Select Tank:"
    tanklabel.pack()

    def tankselected(*args):
        try:
            load_soundingtable("soundingtables/" + tankset.get() +".csv")
        except:
            messagebox.showerror(title=None, message="Sounding Table Format Invalid!")
        
    tankselect = ttk.Combobox(mainwindow)
    tankselect["values"] = tanks
    tankselect["textvariable"] = tankset
    tankselect["state"] = "readonly"
    tankselect.pack(padx=5,pady=5) 
    tankselect.bind("<<ComboboxSelected>>", tankselected)
    
#sounding box frame
    soundingframe = ttk.Frame(mainwindow)

    soundinglabel = ttk.Label(soundingframe)
    soundinglabel["text"] = "Enter Sounding: "
    soundinglabel.pack(side="left")
    
    soundingbox = ttk.Entry(soundingframe)
    soundingbox["width"] = 5
    soundingbox["textvariable"] = soundingset
    soundingbox.pack(side="left")

    soundingframe.pack(pady=5)

#trim frame
    trimframe = ttk.Frame(mainwindow)

    trimlabel = ttk.Label(trimframe)
    trimlabel["text"] = "Trim:"
    trimlabel.pack()
    
    def updatetrimvalues(*args):
        trimselect["values"] = sorted(trimtable.keys())
    
    trimselect = ttk.Combobox(trimframe)
    trimselect["width"] = 5
    trimselect["textvariable"] = trimset
    trimselect["state"] = "readonly"
    trimselect["postcommand"] = updatetrimvalues
    trimselect.pack(padx=5,pady=5)
    trimframe.pack(side="left")
    
    trimset.set("0")

#calculate sounding button
    okbutton = ttk.Button(mainwindow)
    okbutton["text"] = "Sound"
    okbutton["command"] = okclick
    okbutton.pack(pady=5)

#label for sounding input box
    soundingdisplay = ttk.Label(mainwindow)
    soundingdisplay["textvariable"] = displayset
    soundingdisplay.pack()
    
    displayset.set("Tank: \nSounding: \nTrim: \nContents:")

#quit button 
    quitapp = ttk.Button(mainwindow)
    quitapp["text"] = "Quit"
    quitapp["command"] = mainwindow.destroy
    quitapp.pack(pady=5)

#generate sounding table from .csv file format sounding,contents...
def load_soundingtable(file):
    #parse each line and add to soundingtables{}
    inputfile=open(file, "r")
    contents = []
    while True:
         sounding_and_contents = inputfile.readline()
         sounding_and_contents = sounding_and_contents[:-1]
         if not sounding_and_contents:
             break
         else:
             contents = sounding_and_contents.split(",")
             soundingtable[contents[0]] = contents
    inputfile.close()
    
    #get trim values from soundingtable{}
    i=0
    for trim in soundingtable["Trim"]:
        trimtable[trim] = i
        i = i+1
        
    del trimtable["Trim"] 
        
def okclick():
    
    #calculate tank contents
    try:
        trim = trimset.get()
        sounding = soundingset.get()
        tankcontents = soundingtable[sounding][trimtable[trim]]
    except:
        messagebox.showerror(title=None, message="Please Enter Valid Sounding")
        
    #update sounding display
    try:
        displayset.set("Tank: " + tankset.get() +"\nSounding: " + sounding + " cm\nTrim: " + trim +" m\nContents: " + tankcontents + " m3")
    except:
        messagebox.showerror(title=None, message="Please Enter Valid Sounding")

#create widgets
makewidgets()

#mainloop
mainwindow.mainloop()
