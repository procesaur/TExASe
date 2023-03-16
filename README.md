# Text Extraction Api Service - TExASe

## Use GUI
Simply, on the left, pick a file and click process. The result will appear on the right.

Optionally, if you want a more precise OCR, input a language code for tesseract bellow.

## Use API

### url
hostname/api

### required args
**file** : containing filename of the file

### optional args

**lang** : language code for tesseract ocr
**renew** : 1, if you want your file to be replaced with a new one. defult is 0 for False.
    
# Options

Some of the options are configured in the [config.json](config.json) file. 
These include:

**languages** : a list of default languages to be used in OCR.

**log** : string, file location of a writable log file. If the file is specified and writable, all requests will be logged in it.

**redis** : redis server options. If **on** is set to **1**, all requests will go through a redis queue on specified **url** and **port**.
