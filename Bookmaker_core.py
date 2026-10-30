'''
#V1 - Creation of PDF from imgs ✓
#V2 – Bare-bones UI ✓
#V3 - Generating text
#V4 - Option for creating chapters for browsing the PDF
#V5 - Basic text edit
#V6 - Basic PDF edit
#V7 - polish UI
'''


import img2pdf                                      #img to PDF convertor
import tkinter as tk                                #GUI
from tkinter import filedialog, dnd, Button, IntVar #GUI
import os                                           #file manipulation
import glob                                         #file manipulation
import pytesseract                                  #machine-text reading
#from pdf2image import convert_from_path            #conversion from pdf to an img
from PIL import Image, ImageFile                    #img manipulationi
#import re
#import fitz
import shutil

#var/config
ImageFile.LOAD_TRUNCATED_IMAGES = True              #solves pillow errors
root = tk.Tk()                                      #root of main window
imgs = []                                           #array of img to-be-turned into a PDF
dir = ""                                            #location of directory with img
Existence = True                                    #Existence of a PDF for manipulation
page = 1                                            #counter for splitting double pages

choice = tk.IntVar()                                #choice for how much textGen
deuce = tk.IntVar()                                 #option for splitting double pages
bckp = tk.IntVar()                                  #option for creating a backup of the folder with pictures

#functions
    #dir search
def Open():
    global dir

    dir = tk.filedialog.askdirectory(
    #file = tk.filedialog.askopenfilenames(
        title='Select a file...',
        #file=(("jpeg","*.jpg"),("all files","*.*")),       once the OCR and PDF edit is live, this will be used to also search for the PDF
    )
    text.configure(state='normal')
    text.insert(index=1.0, chars=str(dir))
    text.configure(state='disabled')
        #Debug -- turn into a loading bar for V7
    DirDebug.insert(index=1.0,chars='Direcotry found')
    DirDebug.configure(state='disabled')


    #PDF creation
def Cpdf():
    global Cbrnch, Existence, choice, deuce

    #Debug -- turn into a loading bar for V7
    CpdfDebug.insert(index=1.0,chars='Cpdf initialized')
    CpdfDebug.configure(state='disabled')

    Existence = False

    if dir != "":

        Cbrnch = tk.Toplevel(root, bg='gray')
        Cbrnch.title('Create PDF')
        Cbrnch.geometry("200x200")
       # Cbrnch.iconbitmap(default='Icon.png')
        Cbrnch.resizable(width=False, height=False)

        tk.Radiobutton(Cbrnch, text='Plain', variable=choice, value=0, bg='gray').pack(anchor='w')
        tk.Radiobutton(Cbrnch, text='With text only', variable=choice, value=2, bg='gray').pack(anchor='w')
        tk.Radiobutton(Cbrnch, text='With chapters', variable=choice, value=3, bg='gray').pack(anchor='w')  

        tk.StringVar().set('Plain')

        tk.Checkbutton(Cbrnch, text='Split double-pages', variable=deuce, onvalue=1, offvalue=0, bg='gray').pack(anchor='w')
        tk.Checkbutton(Cbrnch, text='Keep folder', variable=bckp, onvalue=1, offvalue=0, bg='gray').pack(anchor='w')

        Ccontinue = tk.Button(Cbrnch, text='Continue', command=Cont).pack(anchor='sw')

    #continuation of Cpdf
def Cont():

    Choice = choice.get()                                                   #conversion has to be done here, else everything breaks
    
        #Debug -- turn into a loading bar for prod
    TvarDebug.insert(index=1.0,chars='Choice='+str(Choice)+',Existence='+str(Existence))
    TvarDebug.configure(state='disabled')
    
    ContDebug.insert(index=1.0,chars='Cont initialized')
    ContDebug.configure(state='disabled')

    Cbrnch.destroy()

    if bckp.get() == 1:
       shutil.copytree(dir, dir + '.bckp') 

    if Existence == False:          #checks the existence of a PDF

        for file in os.listdir(dir):
            if not file.endswith(".jpg"):          
                continue
            path = os.path.join(dir, file)
        #    if os.path.isdir(path):
        #           continue
            imgs.append(path)                                              

        imgs.sort(key=str.lower)    #sorts list numericaly and by length (to tolerate double-page names like "10-11")
        imgs.sort(key=len)

        if deuce.get() == 1:        #splits the double-page if the option was selected
            for img in imgs:
                w, h = Image.open(img).size
                if w > h:
                    Page = Image.open(img)
                    Left = Page.crop((0, 0, w//2, h))
                    Right = Page.crop((w//2, 0, w, h))
                    Left.save(img)
                    Right.save(img + '.jpg')
                    imgs.insert(page, img+'.jpg')
                page += 1

        with open(dir+".pdf","wb") as pdf:
            pdf.write(img2pdf.convert(imgs))

        if deuce == 1:
            for file in os.listdir(dir):
                if file.endswith('.1.jpg'):
                    os.remove(file)

        imgs.clear()                #resets for new creation of PDF
        page = 1
        shutil.rmtree(dir)
        os.rename(dir + '.bckp', dir)

    ContFDebug.insert(index=1.0,chars='Cont finished')
    ContFDebug.configure(state='disabled')

'''
    if Choice != 1:           #if the choice for textGen was chosen, you better start generating text
        txtGen()

    #generování textu
def txtGen():

    Iter = 0

    for imageInFolder in imgs:
        with open(imageInFolder, 'rb') as file:
            img = Image.open(file)
            IMGtext = pytesseract.image_to_string(img, config='--psm 6', lang='ces+eng+jpa')
            with open(str(Iter)+"IMGtext.txt", "a") as IMGtext_file:
                IMGtext_file.write(IMGtext)
                Iter = Iter + 1

    PDFdoc = fitz.open(str(dir)+".pdf")
    pageNum = 0
    page = PDFdoc.load_page(pageNum)

    for Txt in Iter:
        with open(str(Iter)+"IMGtext.txt", "r") as IMGtext_file:
            IMGtext_file.read(Txt)
            page.insert_text((100,100), Txt, fontsize=12, color=(0,0,0)) 
    PDFdoc.save(str(dir)+".pdf")

    
    txtGenDebug.insert(index=1.0,chars='txtGen initialized')
    txtGenDebug.configure(state='disabled')
    
    #if Tvar == 3:                   textGen with highlighted chapters

    #Adding text
def Atxt():
    global Tbrnch

    if dir != "":

        Tbrnch = tk.Toplevel(root, bg="gray")
        Tbrnch.title('Add text')
        Tbrnch.geometry("200x100")
        Tbrnch.iconbitmap(default='Icon.png')
        Tbrnch.resizable(width=False, height=False)

        tk.Radiobutton(Tbrnch, text='With text only', variable=tvar, value=2, bg='gray').pack(anchor='w')
        tk.Radiobutton(Tbrnch, text='With chapters', variable=tvar, value=3, bg='gray').pack(anchor='w')

        Acontinue = tk.Button(Tbrnch, text='Continue', command=txtGen).pack(anchor='sw')
   
    #editing the PDF
def Epdf():
    print('Epdf')
'''

#main window
root.title('Bookmaker')
root.geometry("600x400")
root.configure(bg="gray")
#root.iconbitmap("Icon.ico")  Fix once the main part of the code is functional, proving to be a bit of a problem
root.resizable(width=False, height=False)

#GUI
    #buttons on root
browse = tk.Button(root, heigh = 1, width = 7, text = 'Browse', command=Open)           #Browse
browse.place(x=5,y=5)

createPdf = tk.Button(root, height = 1, width = 7, text='Create PDF', command=Cpdf)     #create PDF
createPdf.place(x=95,y=5)

Edit = tk.Button(root, height = 1, width = 7, text='Edit PDF')#, command=Epdf)          #edits the PDF
Edit.place(x=185,y=5)

addText = tk.Button(root, height = 1, width = 7, text='Add Text')#, command=Atxt)       #Add Text
addText.place(x=275,y=5)

#texts
    #dir text box
text = tk.Text(root, height=1, width=50, font=('Helvetica', 10), state='disabled', bg='gray')
text.place(x=75,y=45)

    #File Path:
FilePthTxt = tk.Text(root, height=1, width=8, font=('Helvetica',10), bg='gray', relief='flat')
FilePthTxt.place(x=5,y=45)
FilePthTxt.insert(index=1.0, chars='File Path:')
FilePthTxt.configure(state='disabled')

    #debug  -> turn into a loading bar (maybe keep the text)
        #directory found
DirDebug = tk.Text(root, height=1, font=('Helvetica',10),bg='gray',relief='flat')
DirDebug.place(x=5,y=75)

        #Cpdf initialized
CpdfDebug = tk.Text(root, height=1, font=('Helvetica',10),bg='gray',relief='flat')
CpdfDebug.place(x=5,y=95)

TvarDebug = tk.Text(root, height=1, font=('Helvetica',10),bg='gray',relief='flat')
TvarDebug.place(x=75,y=95)

        #Cont initialized
ContDebug = tk.Text(root, height=1, font=('Helvetica',10),bg='gray',relief='flat')
ContDebug.place(x=5,y=95)

        #Cont finished
ContFDebug = tk.Text(root, height=1, font=('Helvetica',10),bg='gray',relief='flat')
ContFDebug.place(x=5,y=115)

        #txtGen initialized
txtGenDebug = tk.Text(root, height=1, font=('Helvetica',10),bg='gray',relief='flat')
txtGenDebug.place(x=5,y=135)


#sounds (is it really needed?)

root.mainloop()
