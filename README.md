## Comparing tutorialspoint.com tutorial to video tutorials

## Installation
This code have been developed on a debian based system so for using this on windows maching just look at the section where filename have been mentioned.
And change it accordingly, If you're using mac then You're on your own.

Use following command to install dependency

```bash
pip install -r req.txt
```

Now you need to download some models in nltk, You can simply run 
**import nltk**
**nltk.download(pkgName)**

**there will be link.csv file to give you reference of link from filename**

## This project are divided into several parts

### 1) Downloading data from youtube
    Run gettingSub.py by using following commands and give keywords when asked
    ```python gettingSub.py```
    you can also use this feature in other python script by importing the class ScrapSubs

### 2) Downloading data from tutorialspoint
    Run gettingTut.py by using following commands and give base url like "https://www.tutorialspoint.com/javascript/javascript_overview.htm" when asked
    ```python gettingTut.py```
    you can also use this feature in other python script by importing the class scrapTutorials

### 3) Preprocessing of data
    In preprocessing I'm going through following steps:
        1) Considering subtopics too from a html file from tutorialspoint.com
        2) Converting string to lower
        3) Removing non Alpha-Numeric characters
        4) Removing StepWords
        5) Removing some parts of speech which have no impacts
        6) Removing most common youtube word like "guys", "yeah"...., 
        7) You can get most common youtube words by downloading subtitles from many tutorial and getting distribution from function commonAll()
        8) Stem the word to get the original word so we don't see function, functions different
    File gettingTut.py contains a many relevent functions.
    Function preProcess() will return preprocessed string into string format as well as list format
    you can import functions like this:
**from langProcessing import docParse, preProcess, cwords, subsParse, get_cosine, column**

### 4) Doc_matching
    This is the most common algorithms to compare two documents, Where we get bag of words then see cosine similarity of two documents.
    In this scripts I have also compared heading-heading and haven't normalised the score so don't freak out if you see score more than 1 :p
    Run docSimilarity.py by using following commands it will save results in a csv file where first column consist our tutorialpoints filename and subsequesnt columns represents close yoputube videos
    ```python docSimilarity.py```

### 5) Topic Modeling
    In topic modeling we get a topic from a given document, It used LDA "https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation" model.
    In this scripts I have also compared heading-heading and haven't normalised the score so don't freak out if you see score more than 1 :p
    Run topicSim.py by using following commands it will save results in a csv file where first column consist our tutorialpoints filename and subsequesnt columns represents close yoputube videos
    ```python topicSim.py```


Just check the filename agains link using ref.csv
### As this is totally not labeled data so not have any benchmark to show
### just need to watch the videos from our result in free time and update the algorithm based on feedback
