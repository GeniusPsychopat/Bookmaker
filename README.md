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

So far only Linux compatibility is worked on, but I would like to make it Windows compatible as well. (No clue about the difficulty of this)

## When?
The core part of the code is **done**, as well as the text generation and bookmark preservation. Current efforts are focused on PDF edit, but since the most important part of the code is functional, I'm not gonna make any guarantees. 
The project was shelved for a bit, but I am eager to get it out as soon as possible.

## To-Do list
 - PDF edit
 - Generated-text edit
 - UI overhaul
 - Win compatibility

*Note: None of these are set in stone, if I find that they are out of reach for me, I will drop them.*

## Install and usage
*Note: This app requires git (for cloning the repo) and Python installed on your machine to work*

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
