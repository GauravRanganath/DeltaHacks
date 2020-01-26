# Signatio
A DeltaHacks project

## What does it do?
Uses machine learning and computer vision to gamify and break down the barriers of learning American Sign Language

## How does it do that?
Users will complete modules and unlock levels of higher difficulties that gradually build your ASL skills.
As of now Signatio has:
- An initial module to guide the user through the entire ASL alphabet
- A 2nd module that generates a randomized multiple choice test to help associate between English and ASL alphabets
- A 3rd module that tests the user's mastery of the alphabet by making them sign a letter without any aid

## How was it built?
The interactive educational platform was built using Flask and Bootstrap. We also created and trained a multi-class image classification model to recognize ASL alphabets using a live webcam feed.

## Try it out!

#### 1. Clone the repo (one of the following)

- `git clone git@github.com:GauravRanganath/DeltaHacks.git`
- `git clone https://github.com/GauravRanganath/DeltaHacks.git`

#### 2. Run the file

- `cd DeltaHacks`
- `./server.py` **OR** `python server.py`
- Head to `http://localhost:5000` and access the project 
