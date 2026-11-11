<img width="256" height="256" alt="Icon" src="https://github.com/user-attachments/assets/46874959-9a7a-48a7-922e-3ee88dc347ac" />

# Bookmaker

## What?
Do you have scanned textbooks that are only a loose set of images in a folder?

Do you have book ripped from an internet library that is only just a couple of screenshots?

If yes, then Bookmaker is for you. Currently it lets you choose a folder with images and turns it into a PDF. 
It can also split double pages if you want them page-by-page, or let you create a backup of the folder so you dont lose them.
As of the latest update, the OCR is live. If you have a PDF with already set bookmarks, Bookmaker will save them to a text file, and then automaticaly adds them back.

The actual purpose of this is to let me fill in text into PDFs so I can search through my personal digital library easier, 
but I wanted something fully fleshed-out

## How?
The whole thing is python coded, the OCR is done with pytesseract (a wrapper for Google OCR). I am no profesional, I am mostly learning as I go,
so the code can have some weak links.

## When?
The core part of the code is **done**, including the text generation and bookmark preservation. 
Since the project reached it's intended point, the updates will slow down a bit. Next efforts are gonna be focused on further optimization, edge-case handeling and functionality on Win.
Plans for some light PDF edit (option to manualy fix page ordering and text generation mistakes) and packing the program into an executable, are in the works, but I'm not making any promises. 

## Install and usage
*Note: This app requires git (for cloning the repo) and Python installed on your machine to work.*
*Note 2: Currently tested only on linux, Win is not supported.*

1. Download the zip and extract, or git clone the repo wherever you need it.
```
git clone https://github.com/GeniusPsychopat/Bookmaker.git
```
2. cd into the repo you just got.
```
cd Bookmaker/
```
3. Create a virtual environment and install required libraries.
```
python -m venv Bookmaker
source Bookmaker/bin/activate
pip install -r requirements.txt
```
4. Run the app.
```
python Bookmaker_core.py
```
