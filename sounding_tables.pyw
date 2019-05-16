# -*- coding: utf-8 -*-
"""
This is a sounding table program.

This program uses .csv files in the format 
Trim,value,value,... 
Sounding,contents,contents... 
Sounding,contents,contents... 

files named as Tank.csv in ./sounding_tables/

Created by Joseph Douce
"""
import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk 
from datetime import datetime, date, time
import glob

#import list of tanks from folder /sounding_tables/
tanks = glob.glob('./sounding_tables/*.csv')
      
#setup main_window
main_window = themed_tk.ThemedTk()
main_window.title("Sounding Tables")
main_window.iconbitmap(default='./icon.ico')
main_window.set_theme('arc')

#global variables
sounding_table = {}
trimtable = {}
soundings = {}
contents = {}
previous_values = {}
previous_values_update = {}
date_and_time = {}

#global widget varibales
i=0
for tank in tanks:
    soundings[i] = tk.StringVar()
    date_and_time[i] = tk.StringVar()
    contents[i] = tk.StringVar()
    i=i+1

#slice the path and .csv fom the tank names        
def slice_tanks():
    for i, _ in enumerate(tanks):
        tanks[i] = tanks[i][18:-4]

#make the widgets
def make_widgets():

    #headings
    sounding_frame = ttk.Frame(main_window)
    sounding_frame.pack()
    
    column_one = ttk.Frame(sounding_frame)
    column_one.pack(side="left")

    column_spacer = ttk.Frame(sounding_frame)
    column_spacer["width"] = 10
    column_spacer.pack(side="left")

    column_two = ttk.Frame(sounding_frame)
    column_two.pack(side="left")

    column_spacer = ttk.Frame(sounding_frame)
    column_spacer["width"] = 10
    column_spacer.pack(side="left")

    column_three = ttk.Frame(sounding_frame)
    column_three.pack(side="left")
   
    #tank rows
    for i, _ in enumerate(tanks):

        if tanks[i][0:2] == "BA":
            column = column_two
        elif tanks[i][0:2] == "GW":
            column = column_two
        elif tanks[i][0:2] == "FO":
            column = column_three
        elif tanks[i][0:2] == "DO":
            column = column_three
        else:
            column = column_one
        
        if not tanks[i][:2] == tanks[i-1][:2]:
            type_frame = ttk.Frame(column)
            type_frame.pack()

            type_label = ttk.Label(type_frame)
            type_label["text"] = tanks[i].split(" ")[0]
            type_label.pack() 

        row_frame = ttk.Frame(column)
        row_frame.pack()

        tank_frame = ttk.Frame(row_frame)
        tank_frame.pack(side="left")

        result_frame = ttk.Frame(row_frame)
        result_frame.pack(side="right")

        #individual tank names
        tank_label = ttk.Label(tank_frame)
        tank_label["text"] = tanks[i]
        tank_label["width"] = 20
        tank_label.pack(side="left")

        #individual tank sounding boxes
        sounding_box = ttk.Entry(tank_frame)
        sounding_box["width"] = 5
        sounding_box["textvariable"] = soundings[i]
        sounding_box.pack(side="left")
        sounding_box.bind("<Return>", update_values)
        sounding_box.bind("<Tab>", update_values)

        #cm label
        cm_label = ttk.Label(tank_frame)
        cm_label["text"] = "cm"
        cm_label["width"] = 3
        cm_label.pack(side="left") 

        #spacer label
        spacer_label = ttk.Label(result_frame)
        spacer_label["text"] = ""
        spacer_label["width"] = 2
        spacer_label.pack(side="left")

        #value label
        value_label = ttk.Label(result_frame)
        value_label["textvariable"] = contents[i]
        value_label["width"] = 7
        value_label.pack(side="left")

        #m3 label
        m3_label = ttk.Label(result_frame)
        m3_label["text"] = "m3"
        m3_label["width"] = 3
        m3_label.pack(side="left")

        #datetime label
        date_time_label = ttk.Label(result_frame)
        date_time_label["textvariable"] = date_and_time[i]
        date_time_label.pack(side="left")

    exit_frame = ttk.Frame(main_window)
    exit_frame.pack()

    copyright_frame = ttk.Frame(main_window)
    copyright_frame.pack()

#exit button 
    exit_button = ttk.Button(exit_frame)
    exit_button["text"] = "Exit"
    exit_button["command"] = main_window.destroy
    exit_button.pack(pady=5, side="left")

    refresh_button = ttk.Button(exit_frame)
    refresh_button["text"] = "Refresh"
    refresh_button["command"] = update_values
    refresh_button.pack(pady=5, side="left")

    report_button = ttk.Button(exit_frame)
    report_button["text"] = "Create Report"
    report_button["command"] = output_report_file
    report_button.pack(pady=5, side="left")

    copyright_label = ttk.Label(copyright_frame)
    copyright_label["text"] = "© Joseph Douce 2018"
    copyright_label.pack()

#select tank to be calculated
def tank_selected(tank):
    try:
        load_sounding_table("sounding_tables/" + tank +".csv")
    except:
        pass

#generate sounding table from .csv file
def load_sounding_table(file):
    
    #parse each line and add to sounding_tables{}
    input_file=open(file, "r")
    contents = []
    while True:
         sounding_and_contents = input_file.readline()
         sounding_and_contents = sounding_and_contents[:-1]
         if not sounding_and_contents:
             break
         else:
             contents = sounding_and_contents.split(",")
             sounding_table[contents[0]] = contents
    input_file.close()
    
    #get trim values from sounding_table{}
    i=0
    for trim in sounding_table["Trim"]:
        trimtable[trim] = i
        i = i+1
        
    del trimtable["Trim"] 

#write new values to output file            
def update_values(*args):
    #check if anyone else has updated values from file
    update_ui("refresh")
    #write new values to file
    output_to_file()
    #after writing values to file update ui with new values
    update_ui("load")

#update displayed values from input file
def update_ui(state):
    input_file=open('./sounding_tables/last_soundings.txt', "r")
    i=0
    while True:
         sounding_and_time = input_file.readline()
         sounding_and_time = sounding_and_time[:-1]
         if not sounding_and_time:
             break
         else:
             values = sounding_and_time.split(",")
             if state == "load":
                 previous_values[i] = values
                 #sounding
                 soundings[i].set(previous_values[i][1])
                 #datetime
                 date_and_time[i].set(previous_values[i][2])
                 tank_selected(tanks[i])
                 try:
                     contents[i].set(sounding_table[soundings[i].get()][trimtable["0"]])
                 except:
                     contents[i].set("ERR")
             elif state == "refresh":
                 previous_values_update[i] = values
                 if not previous_values_update[i] == previous_values[i]:
                     #sounding
                     soundings[i].set(previous_values_update[i][1])
                     #datetime
                     date_and_time[i].set(previous_values_update[i][2])
                     tank_selected(tanks[i])
                     try:
                         contents[i].set(sounding_table[soundings[i].get()][trimtable["0"]])
                     except:
                         contents[i].set("ERR") 
             i=i+1
    input_file.close()

def output_to_file(*args):
    output_file=open('./sounding_tables/last_soundings.txt', 'w')
    for i, _ in enumerate(soundings):
        try:
            if soundings[i].get() == previous_values[i][1]:
                print(tanks[i] + ',' + previous_values[i][1] + ',' + previous_values[i][2], file=output_file)
            else:
                print(tanks[i] + ',' + soundings[i].get() + ',' + str(datetime.today())[:-10], file=output_file)
        except:
            print(tanks[i] + ',' + soundings[i].get() + ',' + str(datetime.today())[:-10], file=output_file)
    output_file.close()

def output_report_file(*args):
    output_file=open('./sounding_reports/Sounding Report ' + str(datetime.today())[:-13] + str(datetime.today())[-12:-10] + '.csv', 'w')
    for i, _ in enumerate(soundings):
        print(tanks[i] + ',' + contents[i].get() + ',m3,' + date_and_time[i].get(), file=output_file)
    output_file.close()
    
#trim tank names
slice_tanks()

#create widgets
make_widgets()

#load last soundings file
update_ui("load")

#mainloop
main_window.mainloop()
