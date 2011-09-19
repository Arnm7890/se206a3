#!/usr/bin/python

# SOFTENG 206 Assignment 3
# Andrew Luey and Arunim Talwar
# Date: September 2011


from os import killpg, setsid, getpgid
from subprocess import Popen, PIPE
from signal import signal, SIGKILL
from functools import partial
from Tkinter import Tk, Frame, Button, Listbox, OptionMenu, Scrollbar,
                    StringVar


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
    btn = Button(parent, text=txt, command=fn, bg=colour, width=10)
    btn.grid(column=x, row=y)
    return btn

def CreateOptionMenu(parent, x, y, val, var):
    """ Option menu to show the spelling list """
    optMenu = OptionMenu(parent, val, *var)
    optMenu.grid(column=x, row=y, columnspan=2, sticky="ew")
    return optMenu
    
def CreateListBox(parent, x, y, val):
    """ Listbox to show the spelling list """
    lstbox = Listbox(parent, listvariable=val, selectmode="extended")
    lstbox.grid(column=x, row=y)
    sbar = Scrollbar(parent, orient="vertical", command=lstbox.yview)
    sbar.grid(column=x+1, row=y, sticky="ns")
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
root.title("Teacher Interface")
listFrame = Frame(root, width=200, height=200)
listFrame.grid(column=0, row=0, padx=10, pady=10)

# Word lists
listNames = ["Child", "ESOL", "BEE"]
childList = ("apple", "ball", "cat")
esolList = ("digger", "emu", "fish")
beeList = ("goat", "ho", "igloo")

# Listbox
wordList = StringVar()
CreateListBox(listFrame, 0, 1, wordList)

# Combobox
currentListName = StringVar(value="Please select a list")
optMenu = CreateOptionMenu(listFrame, 0, 0, currentListName, listNames)
#combo.bind('<Child>', lambda: speak("this function will speak any add a new list to the combobox"))
#combo.bind('ESOL', partial(ChangeWordList,esolList))
#combo.bind('BEE', lambda: ChangeWordList(beeList))

# List buttons
#CreateButton(root, 20, 11, "Create list", lambda: speak("this function will speak any add a new list to the combobox"), colour="yellow")
#CreateButton(root, 20, 12, "Remove list", lambda: speak("this function will speak any remove a list from the combobox"), colour="yellow")
#CreateButton(root, 20, 13, "Import list", lambda: speak("this function will speak import a tldr file"), colour="yellow")
#CreateButton(root, 20, 14, "Export list", lambda: speak("this function will speak write a list to a tldr file"), colour="yellow")

# Word buttons
#CreateButton(root, 20, 21, "Add word", lambda: speak("this function will add a word to the list"), colour="green")
#CreateButton(root, 20, 22, "Remove word", lambda: speak("this function will remove a word from the list"), colour="green")
#CreateButton(root, 20, 23, "Add words from another list", lambda: speak("this function will allow you to add words from other lists"), colour="green")

# Speech buttons
CreateButton(listFrame, 0, 2, "Speak selected", lambda: speak("this function will speak any selected words"), colour="red")
CreateButton(listFrame, 0, 3, "Speak all", lambda: speak("this function will speak all the words"), colour="red")
CreateButton(listFrame, 0, 4, "Stop speech", restartFest, colour="red")

root.mainloop()
