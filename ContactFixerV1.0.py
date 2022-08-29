#!/usr/bin/env python3  
# -*- coding: utf-8 -*- 
#----------------------------------------------------------------------------
# Created By  : Andree Renteria Perez
# Created Date: 13/03/2015
# version ='1.0'
# ---------------------------------------------------------------------------
# This program was originally written in Python2.X and its purpose is to
# remove the contact duplicates and trying to align the values with the 
# corresponding field (i.e put email address in the email field, sometimes
# it was typed in the wrong field to save time) and making sure to preserve
# the notes information.
# --------------------------------------------------------------------------- 

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import re
import linecache
import csv
import itertools
import os
import math
import csv
import collections
import numpy as np
from pprint import pprint
import time

#Csv FileName
myFile = ""
myFilePath = ""
csvFilename = ""
csvFile = ""
startDedupeBool = False

#Start Tkinter
root = Tk()
root.title("ContactFixer")

#Define Frames inside window
FileSelectionFrame = Frame(root)
FileSelectionFrame.pack()

statusFrame = Frame(root)
statusFrame.pack()

consoleFrame = Frame(root)
consoleFrame.pack()

#Button Text Variable
startDedupeText = "Run"

#Create Functions to Execute

#Usefull Functions
def modified(self, event):
    self.txt.see(END)  # tkinter.END if you use namespaces
    
#Select File to Dedupe
def SelectCsv():
    global csvFile
    global myFilePath
    
    #Define File Extension
    csvFile = filedialog.askopenfile(
                                    "r", 
                                    filetypes=[("CSV Files","*.csv")]
                                    )

    #Make String Copy to display
    myFilePath = str(csvFile)
    
    #Parse Path Information
    myFilePath = myFilePath.split("'", 1)[1].split("'")[0]
    
    #Print GUI Entry
    pathText.insert(END, myFilePath)
    
    #Print selected to console
    print("The file: " + myFilePath + " was succesfully added.")

    printConsoleSeparator() 
    consoleView.insert(
                        END, 
                        "The CSV file: " + 
                        myFilePath + 
                        " was added succesfully.\n"
                        )

def printConsoleSeparator():
    for i in range(92):
        consoleView.insert(END, "-")
    consoleView.insert(END, "\n")


def dedupeRoutine():
    try:
        #Loop Counter
        loopCounter = 0
        progressCounter = 0.0

        #Change text to STOP in GUI
        #startDedupeText = "Detener"
        
        #Define input file parameters
        data = []
        
        def unique():
           
            with open(myFilePath, "r", encoding = 'latin-1') as csvFileOpen:

                rows = csv.DictReader(csvFileOpen)

                for row in rows:
                    print("The number of columns in the CSV file is: " + \
                            str(len(row.keys()))) 
                    
                    print(row.values())

                    time.sleep(1)
                
                return result.values()
        
        data.append(unique())
        
        print(len(data[0]))

        printConsoleSeparator()  
        consoleView.insert(END, "Searching Unique Records.\n")
        
        printConsoleSeparator() 
        consoleView.insert(
                            END, 
                            "Unique Records Found: " + 
                            str(len(data[0]) - 1) + 
                            "\n"
                        )
        
        combinationCalculation = len(data[0])
        
        outputFile = os.path.dirname(myFilePath)
        print(outputFile)
        outputFile = outputFile + "/DedupedCSVFile.csv"
        print(outputFile)
        
        writer = csv.writer(open(outputFile, "wb"))
            
        rowNumber = 0
            
        for row in data:
            writer.writerows(row)
            for item in row:
                rowNumber = rowNumber + 1
                for i in item:
                    consoleView.insert(
                                        END, 
                                        "Comparando Registro " + 
                                        str(rowNumber) + 
                                        " de " + 
                                        str(len(data[0])) + 
                                        " : " + 
                                        str(i) + "\n"
                    )
                    
                    #Update Progress Bar
                    loopCounter = loopCounter + 1
                    #print loopCounter
                    
                    progressCounter = (
                                        float(rowNumber)/                   \
                                        float(combinationCalculation)) *    \
                                        100.0
                    print(progressCounter)
                    
                    progressbar["value"] = progressCounter
                
                consoleView.see("end")
                    
                root.update_idletasks()
                root.update()
        
        printConsoleSeparator() 
        consoleView.insert(END, "Closing CSV file: OK! \n")
        
        printConsoleSeparator() 
        consoleView.insert(END, "File exported: " + outputFile + "\n")

        printConsoleSeparator() 
        consoleView.see("end")
        
                    
        #Close Deduped CSV File    
        csvFile.close()
        
    except IOError:
        
        print("No file was selected, please select a file.")
        consoleView.insert(
                            END, 
                            """No Contacts file was selected.
                            Please select a Contacts file with 
                            extension ".csv"\n"""
                        )
        
#Create Buttons to Interact in GUI
#Select input file
fileSelectionSubFrame = LabelFrame(
                            FileSelectionFrame, 
                            text="Select Agenda", 
                            padx = 5, 
                            pady= 5
                        )
    
selectCsvButton = Button(
                        fileSelectionSubFrame, 
                        text="Choose CSV", 
                        command = SelectCsv
                    ) 

pathText = Entry(
                fileSelectionSubFrame, 
                width = 60
            )
#Progress Bar
#LabelFrame
progressLabel = LabelFrame(
                        statusFrame, 
                        text="Progress", 
                        padx = 5, 
                        pady= 5
                )
#Label
progressLabelText = Label(progressLabel, text="Status:")
#Progress Bar
progressbar = ttk.Progressbar(
                                progressLabel, 
                                orient=HORIZONTAL, 
                                length=557, 
                                mode='determinate'
                            )

progressbar["maximum"] = 100
#progressbar.start()
progressbar["value"] = 0
#Dedupe Button
startDedupeButton = Button(
                            progressLabel, 
                            text= startDedupeText, 
                            command = dedupeRoutine 
                    )
#Dedupe Stop Button
#Console View
consoleLabel = LabelFrame(consoleFrame, text="Console", padx = 5, pady= 5)
scrollConsole = Scrollbar(consoleLabel)
consoleView = Text(
                    consoleLabel, 
                    width = 92, 
                    height = 10, 
                    yscrollcommand = scrollConsole.set
                )
#Greeting 
consoleView.insert(END, "Welcome to ContactFixer V1.0!\n")

#Pack windows
#File Selection
fileSelectionSubFrame.pack()
selectCsvButton.pack(side=RIGHT)
pathText.pack(side=LEFT)
#Progress And Start Button
progressLabel.pack()
progressLabelText.pack(side=LEFT)
progressbar.pack(side=LEFT)
startDedupeButton.pack(side=RIGHT)
#Console
consoleLabel.pack()
scrollConsole.pack(side=RIGHT, fill = Y)
scrollConsole.config( command = consoleView.yview )
consoleView.pack(side=LEFT, fill=BOTH)

root.mainloop()
