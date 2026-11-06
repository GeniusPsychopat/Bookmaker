'''
V1 - Creation of PDF from imgs ✓
V2 – Bare-bones UI ✓
V3 - Generating text ✓
V4 - Basic PDF edit
V5 - Basic Text edit 
V6 - Creating Table of Contents through PdfEdit
V7 - polish UI
'''


import img2pdf                                      #img to PDF convertori
from pdf2image import convert_from_path
import tkinter as tk                                #GUI
from tkinter import filedialog, dnd, Button, IntVar #GUI
import os                                           #file manipulation
import glob                                         #file manipulation
import pytesseract                                  #machine-text reading
from PIL import Image, ImageFile                    #img manipulationi
import shutil
from pypdf import PdfWriter

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

#var/config
ImageFile.LOAD_TRUNCATED_IMAGES = True              #solves pillow errors
root = tk.Tk()                                      #root of main window
imgs = []                                           #array of img to-be-turned into a PDF
dir = ""                                            #location of directory with img
PDF = ""                                            #location of PDF
PDF_name = ""                                       #name of the PDF
Existence = True                                    #Existence of a PDF for manipulation
page = 1                                            #counter for splitting double pages
pdfs = []                                           #array of pages of PDF to-be-turned into a single PDF

choice = tk.IntVar()                                #choice for how much textGen
deuce = tk.IntVar()                                 #option for splitting double pages
bckp = tk.IntVar()                                  #option for creating a backup of the folder with pictures

#functions
    #dir search
def Open():
    global dir

    dir = tk.filedialog.askdirectory(title='Select a directory...')

    text.configure(state='normal')
    text.insert(index=1.0, chars=str(dir))
    text.configure(state='disabled')

        #Debug -- turn into a loading bar for V7
    txtDebug.configure(state='normal')
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0,chars='Directory found')
    txtDebug.configure(state='disabled')


    #PDF creation
def Cpdf():
    global Cbrnch, Existence, choice, deuc

    #Debug -- turn into a loading bar for V7
    txtDebug.configure(state='normal')
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0,chars='Cpdf initialized')
    txtDebug.configure(state='disabled')

    Existence = False

    if dir != "":

        Cbrnch = tk.Toplevel(root, bg='gray')
        Cbrnch.title('Create PDF')
        Cbrnch.geometry("200x100")
       # Cbrnch.iconbitmap(default='Icon.png')
        Cbrnch.resizable(width=False, height=False)

        tk.Checkbutton(Cbrnch, text='Generate text', variable=choice, onvalue=1, offvalue=0, bg='gray').pack(anchor='w')
        tk.Checkbutton(Cbrnch, text='Split double-pages', variable=deuce, onvalue=1, offvalue=0, bg='gray').pack(anchor='w')
        tk.Checkbutton(Cbrnch, text='Keep folder', variable=bckp, onvalue=1, offvalue=0, bg='gray').pack(anchor='w')

        Ccontinue = tk.Button(Cbrnch, text='Continue', command=Cont).pack(anchor='sw')

    #continuation of Cpdf
def Cont():

    Choice = choice.get()                                                   #conversion has to be done here, else everything breaks

        #Debug -- turn into a loading bar for prod
    txtDebug.configure(state='normal')    
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0,chars='Cont initialized')
    txtDebug.configure(state='disabled')

    Cbrnch.destroy()
    Cbrnch.update()

    if bckp.get() == 1:
       shutil.copytree(dir, dir + '.bckp') 

    page = 1

    for file in os.listdir(dir):
        if not file.endswith(".jpg"):          
            continue
        path = os.path.join(dir, file)
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

    if choice.get() == 1:
        txtGen()

    if choice.get() == 0:
        for img in imgs:
            with open(dir+'.pdf','wb') as pdf:
                pdf.write(img2pdf.convert(imgs))

    imgs.clear()                #resets for new creation of PDF
    shutil.rmtree(dir)
    if bckp.get() == 1:
        os.rename(dir + '.bckp', dir)

    #Debug -- turn into a loading bar for prod
    txtDebug.configure(state='normal')
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0,chars='Cont finished')
    txtDebug.configure(state='disabled')

    #Generating text
def txtGen():

    merge = PdfWriter()
    p = 1

    for img in imgs:
        with open(dir+str(p)+'.pdf', 'w+b') as pdf:
            pdf.write(pytesseract.image_to_pdf_or_hocr(img, extension='pdf', lang='ces+eng'))
            pdfs.append(dir+str(p)+'.pdf')
        p += 1

    txtDebug.configure(state='normal')
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0,chars='Text generated')
    txtDebug.configure(state='disabled')

    for pdf in pdfs: 
        merge.append(pdf)

    if Existence == False:
        merge.write(dir+'.pdf')
    else:
        merge.write(PDF_name)
        shutil.rmtree(dir)
    merge.close()

    for pdf in pdfs:
        os.remove(pdf)
    pdfs.clear()

def Atxt():
    
    PDF = tk.filedialog.askopenfilename(title='Select a PDF...', defaultextension='.pdf', filetypes=[('PDFs','*.pdf')])
    PDF_name = PDF
    os.mkdir(PDF+'.')
    dir = PDF+'.'

    print(PDF_name)

    txtDebug.configure(state='normal')
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0,chars='PDF found, preparing for txtGen')
    txtDebug.configure(state='disabled')

    root.update()

    Existence = True

    convert_from_path(PDF, output_folder=dir, fmt='jpeg')

    os.remove(PDF)

    for img in os.listdir(dir):
        path = os.path.join(dir, img)
        imgs.append(path)

    txtDebug.configure(state='normal')
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0,chars='PDF prepared for txtGen')
    txtDebug.configure(state='disabled')

    root.update()

    txtGen()

'''
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

addText = tk.Button(root, height = 1, width = 7, text='Add Text', command=Atxt)       #Add Text
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
txtDebug = tk.Text(root, height=1, font=('Helvetica',10), bg='gray', relief='flat')
txtDebug.place(x=5,y=75)

#sounds (is it really needed?)

root.mainloop()
