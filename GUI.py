#!/usr/bin/python

# SOFTENG 206 Assignment 2
# Andrew Luey (alue004)
# ID#: 1507807
# Date: August 2011


from os import killpg, setsid, getpgid
from subprocess import Popen, PIPE
from signal import signal, SIGKILL
from functools import partial
from Tkinter import *
from ttk import Combobox


# Speech functions

def speak(text):
    """ Speaks the string input """
    proc.stdin.write('(SayText "%s")\n' % text)

def restartFest():
    """ Stops the current speech """
    global proc
    killpg(getpgid(proc.pid), SIGKILL)
    proc = Popen(["festival", "--pipe"], stdin=PIPE, preexec_fn=setsid)
    
    
# Widget creation functions
    
def CreateButton(parent, x, y, txt, fn, colour):
    """ Button which runs the function fn when pressed """
    btn = Button(parent, text=txt, command=fn, bg=colour, width=20)
    btn.grid(column=x, row=y, sticky="w", padx=10, pady=4)
    return btn

def CreateCombo(parent, x, y, val, elements):
    """ Listbox to show the spelling list """
    combo = Combobox(root, textvariable=val, values=elements)
    combo.grid(column=10, columnspan=2, row=10, sticky="s")
    return combo
    
def CreateListBox(parent, x, y, val):
    """ Listbox to show the spelling list """
    lstbox = Listbox(parent, listvariable=val, selectmode="extended")
    lstbox.grid(column=x, row=y, rowspan=30, sticky="ns")
    sbar = Scrollbar(parent, orient="vertical", command=lstbox.yview)
    sbar.grid(column=x+1, row=y, rowspan=30, sticky="ns")
    lstbox['yscrollcommand'] = sbar.set
    return lstbox

def ChangeWordList():
    global wordList
    wordList.set(childList)


# Start the speaking functionality
proc = Popen(["festival", "--pipe"], stdin=PIPE, preexec_fn=setsid)
proc.stdin.write("(audio_mode 'async)\n")

# Initialise GUI
root = Tk()
root.title("<INSERT TITLE HERE>")

# Word lists
listNames = ["Child", "ESOL", "BEE"]
childList = ("apple", "ball", "cat")
esolList = ("digger", "emu", "fish")
beeList = ("goat", "ho", "igloo")

# Listbox
wordList = StringVar(value=esolList)
CreateListBox(root, 10, 11, wordList)

# Combobox
currentListName = StringVar()
combo = CreateCombo(root, 10, 10, currentListName, listNames)
#combo.bind('<Child>', lambda: speak("this function will speak any add a new list to the combobox"))
#combo.bind('ESOL', partial(ChangeWordList,esolList))
#combo.bind('BEE', lambda: ChangeWordList(beeList))

# List buttons
CreateButton(root, 20, 11, "Create list", lambda: speak("this function will speak any add a new list to the combobox"), colour="yellow")
CreateButton(root, 20, 12, "Remove list", lambda: speak("this function will speak any remove a list from the combobox"), colour="yellow")
CreateButton(root, 20, 13, "Import list", lambda: speak("this function will speak import a tldr file"), colour="yellow")
CreateButton(root, 20, 14, "Export list", lambda: speak("this function will speak write a list to a tldr file"), colour="yellow")

# Word buttons
CreateButton(root, 20, 21, "Add word", lambda: speak("this function will add a word to the list"), colour="green")
CreateButton(root, 20, 22, "Remove word", lambda: speak("this function will remove a word from the list"), colour="green")
CreateButton(root, 20, 23, "Add words from another list", lambda: speak("this function will allow you to add words from other lists"), colour="green")

# Speech buttons
CreateButton(root, 20, 31, "Speak selected", lambda: speak("this function will speak any selected words"), colour="red")
CreateButton(root, 20, 32, "Speak all", lambda: speak("this function will speak all the words"), colour="red")
CreateButton(root, 20, 33, "Stop speech", restartFest, colour="red")

root.mainloop()
