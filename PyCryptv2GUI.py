#Encryption Function

def Encrypt():
    Encryption_Code = textbox3.get()
    Line = textbox1.get()
    Encrypted = ""
    while len(Encryption_Code) < len(Line):
        Encryption_Code += Encryption_Code
    for x in range(len(Line)):
        lttrnum = ord(Line[x])
        wrdnum = ord(Encryption_Code[x])
        encnum = lttrnum * wrdnum
        Encrypted += str(len(str(encnum))) + str(encnum)
    textbox4.delete(0, END)
    textbox4.insert(0, Encrypted)

#Decryption Function

def Decrypt():
    Decryption_Code = textbox3.get()
    Line = textbox2.get()
    Decrypted = ""
    x = 0
    while len(Line) > 0:
        numlen = Line[0]
        Line = Line[1:]
        encnum = int(Line[:int(numlen)])
        Line = Line[int(numlen):]
        try:
            wrdnum = ord(Decryption_Code[x])
        except:
            Decryption_Code += Decryption_Code
            wrdnum = ord(Decryption_Code[x])
        x += 1
        conv = int(encnum) / int(wrdnum)
        Decrypted += chr(int(conv))
    textbox4.delete(0, END)
    textbox4.insert(0, Decrypted)

from tkinter import *

gui = Tk()
gui.geometry("380x105")
gui.title("PyCryptV3")

btn1 = Button(gui, text = "Encrypt", width = 7, command = Encrypt)
btn2 = Button(gui, text = "Decrypt", width = 7, command = Decrypt)

textbox1 = Entry(gui, width = 50)
textbox2 = Entry(gui, width = 50)
textbox3 = Entry(gui, width = 7)
textbox4 = Entry(gui, width = 53)

label1 = Label(gui, text = "Encryption Code:")
label2 = Label(gui, text = "Result:")

label1.place(x = 0, y = 0)
label2.place(x = 0, y = 80)
textbox1.place(x = 67, y = 27)
textbox2.place(x = 67, y = 54)
textbox3.place(x = 100, y = 2)
textbox4.place(x = 50, y = 82)
btn1.place(x = 0, y = 25)
btn2.place(x = 0, y = 50)

gui.mainloop()
