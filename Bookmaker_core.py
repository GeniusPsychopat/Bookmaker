'''
V1 - Creation of PDF from imgs ✓
V2 – Bare-bones UI ✓
V3 - Generating text ✓
V4 - Creating Table of Contents through PdfEdit ✓
V5 - Basic PDF edit
V6 - polish UI
V7 - pack into an executable
'''


import img2pdf                                      #img to PDF convertor
from pdf2image import convert_from_path
import tkinter as tk                                #GUI
from tkinter import filedialog, dnd, Button, IntVar #GUI
import os                                           #file manipulation
import glob                                         #file manipulation
import pytesseract                                  #machine-text reading
from pdf2image import convert_from_path             #conversion from pdf to an img
from PIL import Image, ImageFile                    #img manipulationi
from pypdf import PdfWriter, PdfReader              #PDF manipulation
from typing import List, Union                 
import shutil
import re

from pypdf.generic import Destination
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
Existence = True                                    #Existence of a PDF for manipulation
page = 1                                            #counter for splitting double pages
pdfs = []                                           #array of pages of PDF to-be-turned into a single PDF

choice = tk.IntVar()                                #choice for how much textGen
deuce = tk.IntVar()                                 #option for splitting double pages
bckp = tk.IntVar()                                  #option for creating a backup of the folder with pictures

#functions
    #img sort
def img_sort(s):
    directory = s[len(dir)+1:]
    match = re.split('\\D', directory)
    return int(match[0])

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
    global Cbrnch, Existence, choice, deuce

    #Debug -- turn into a loading bar for V7
    txtDebug.configure(state='normal')
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0,chars='Cpdf initialized')
    txtDebug.configure(state='disabled')

    Existence = False

    if dir != "":
        
        Cbrnch = tk.Toplevel(root, bg='gray')
        Cbrnch.title('Create PDF')
        Cbrnch.geometry("200x115")
        Cbrnch.resizable(width=False, height=False)

        tk.Checkbutton(Cbrnch, text='Generate text', variable=choice, onvalue=1, offvalue=0, bg='gray').pack(anchor='w')
        tk.Checkbutton(Cbrnch, text='Split double-pages', variable=deuce, onvalue=1, offvalue=0, bg='gray').pack(anchor='w')
        tk.Checkbutton(Cbrnch, text='Keep folder', variable=bckp, onvalue=1, offvalue=0, bg='gray').pack(anchor='w')

        Ccontinue = tk.Button(Cbrnch, text='Continue', command=Cont).pack(anchor='sw')

    #continuation of Cpdf
def Cont():
    global imgs

    Choice = choice.get()                                                   #conversion has to be done here, else everything breaks
    
        #Debug -- turn into a loading bar for prod
    txtDebug.configure(state='normal')    
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0,chars='Pre-processing initialized')
    txtDebug.configure(state='disabled')

    Cbrnch.destroy()
    Cbrnch.update()

    if bckp.get() == 1:
       shutil.copytree(dir, dir + '.bckp') 

    for file in os.listdir(dir):
        if not file.endswith(".jpg"):          
            continue
        path = os.path.join(dir, file)
        imgs.append(path)                                 

    try: imgs.sort(key=img_sort)                           #tries to sort pages, if the naming is inconsistent the error will pop up
    except ValueError:
        print('Inconsistent or bad naming scheme')
        raise SystemExit

    page = 1
    if deuce.get() == 1:        #splits the double-page if the option was selected

        txtDebug.configure(state='normal')
        txtDebug.delete('1.0','end')
        txtDebug.insert(index=1.0,chars='Spliting pages')
        txtDebug.configure(state='disabled')

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

    if choice.get() == 1:       #generates text if the option was selected..
        txtGen()
    else:                       #..if not, stitches the double pages
        for img in imgs:
            with open(dir+'.pdf','wb') as pdf:
                pdf.write(img2pdf.convert(imgs))

        #resets for creation of a new PDF
    imgs.clear()
    shutil.rmtree(dir)
    if bckp.get() == 1:
        os.rename(dir + '.bckp', dir)

    #Debug -- turn into a loading bar for prod
    txtDebug.configure(state='normal')
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0,chars='PDF created')
    txtDebug.configure(state='disabled')

    #Generating text
def txtGen():       #average time for txtGen is 13 pages per minute, add a countdown for V7

    merge = PdfWriter()
    p = 1
    counter = 2
    lenght = len(imgs)
        
        #generates text in individual PDFs
    for img in imgs:
        with open(dir+str(p)+'.pdf', 'w+b') as pdf:
            pdf.write(pytesseract.image_to_pdf_or_hocr(img, extension='pdf', lang='ces+eng'))
            pdfs.append(dir+'/'+str(p)+'.pdf')
        p += 1
        
        if p % 2 == 0:
            txtDebug.configure(state='normal')
            txtDebug.delete('1.0','end')
            txtDebug.insert(index=1.0,chars='Generating text ('+ str(counter) + '/' + str(lenght) +')')
            txtDebug.configure(state='disabled')
            root.update()
            counter += 2

    txtDebug.configure(state='normal')
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0,chars='Text generated')
    txtDebug.configure(state='disabled')

        #stitches the pages together
    for pdf in pdfs: 
        merge.append(pdf)

    if Existence == False:          #saving output depending on if the PDF was generated or not
        merge.write(dir+'.pdf')
    else:
        merge.write(PDF)
        shutil.rmtree(dir)

    merge.close()

    for pdf in pdfs:                #cleans up
        os.remove(pdf)
    pdfs.clear()

    #Proccessing and post-processing a PDF for txtGen
def Atxt():
    global PDF, Existence, dir
      
      #selecting a PDF
    PDF = tk.filedialog.askopenfilename(title='Select a PDF...', 
                                        defaultextension='.pdf', 
                                        filetypes=[('PDFs','*.pdf')]
                                        )
    os.mkdir(PDF+'.')
    dir = PDF+'.'

    txtDebug.configure(state='normal')
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0, chars='PDF found, preparing for txtGen')
    txtDebug.configure(state='disabled')
    root.update()

    reader = PdfReader(PDF)
    cOutline(reader.outline, reader)

        #preparing the PDF for OCR
    Existence = True
    convert_from_path(PDF, output_folder=dir, fmt='jpeg')
    os.remove(PDF)
    for img in os.listdir(dir):
        path = os.path.join(dir, img)
        imgs.append(path)
    imgs.sort(key=str.lower)

    txtDebug.configure(state='normal')
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0,chars='PDF prepared for txtGen')
    txtDebug.configure(state='disabled')
    root.update()

    txtGen()

        #adding back the Table of Contents
    writer = PdfWriter(clone_from=PDF)
    with open(PDF+'.txt') as file:      #recovering Table of Contents
        for line in file.readlines():
            if int(line[0]) == 0:
                headline = writer.add_outline_item(title=line[5:], page_number=int(line[1:5]))

            elif int(line[0]) == 1:
                sub_headline = writer.add_outline_item(title=line[5:], page_number=int(line[1:5]), parent=headline)

            elif int(line[0]) == 2:
                writer.add_outline_item(title=(line[5:]), page_number=int(line[1:5]), parent=sub_headline)

        if len(file.readlist()) == 0:
            txtDebug.configure(state='normal')
            txtDebug.delete('1.0','end')
            txtDebug.insert(index=1.0, chars='Table of Contents added')
            txtDebug.configure(state='disabled')
            root.update()

    writer.write(PDF)
    os.remove(PDF+'.txt')

    #Preservetaion of Table of Contents
def cOutline(outline: List[Union[Destionation, List[Destination]]],
              reader: PdfReader,
              level: int = 0
              ) -> None:

            #strips the Table of Contents info from the PDF
    with open(PDF+'.txt', 'w') as o:
        for item in outline:
            if isinstance(item, list):
                cOutline(item, reader, level+1)
            else:
                pageNum = reader.get_destination_page_number(item)
                depth = 1 * level

                if pageNum is None:
                    continue
                else:
                    o.append(str(depth) + '%04d'%pageNum + item.title)

    txtDebug.configure(state='normal')
    txtDebug.delete('1.0','end')
    txtDebug.insert(index=1.0, chars='Table of Contents preserved')
    txtDebug.configure(state='disabled')
    root.update()

'''
    #editing the PDF
def Epdf():
    print('Epdf')
'''

#main window
root.title('Bookmaker')
root.geometry("600x400")
root.configure(bg="gray")
root.iconphoto(True, tk.PhotoImage(file="Icon.png"))  #Fix once the main part of the code is functional, proving to be a bit of a problem
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
text = tk.Text(root, height=1, width=63, font=('Helvetica', 10), state='disabled', bg='gray')
text.place(x=74,y=45)

    #File Path:
FilePthTxt = tk.Text(root, height=1, width=8, font=('Helvetica',10), bg='gray', relief='flat')
FilePthTxt.place(x=5,y=45)
FilePthTxt.insert(index=1.0, chars='File Path:')
FilePthTxt.configure(state='disabled')

    #debug  -> turn into a loading bar (maybe keep the text)
txtDebug = tk.Text(root, height=1, width=72, font=('Helvetica',10), bg='gray', relief='flat')
txtDebug.place(x=5,y=75)

#sounds (is it really needed?)

root.mainloop()
