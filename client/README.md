# This file sends a POST request to the django webserver

 It is not completely download-and-play, since the amount of data I used was a very large set.


## The Data is not included in this directory. To get it locally:

#### 1. Go to https://www.kaggle.com/c/dogs-vs-cats

#### 2. Go to the "data" tab

#### 3. Download the "train.zip" file. There are 12500 cat images and 12500 dog images. 
##### Each file name should be formatted as such, in this order, separated by a . :
- Start with either cat or dog. 
- An integer from 0-12499.
- file type

**Example**: cat.1234.jpg

I originally downloaded the "test.zip" file, and then had a script to 
prepend the "cat." and "dog." to the file name. If for whatever reason the 
data in "train.zip" does not work with the code, try downloading "test.zip"
and prepending cat. and dog. where needed.


### Once you have the data locally:
Create a folder in client called **train**. Put the data in the **train** folder. 

## To Run:
Run `python client.py`