# Text Extraction Api Service - TExASe

## Use GUI
Simply, on the left, pick a file and click process. The result will appear on the right.

Optionally, if you want a more precise OCR, input a language code for tesseract bellow.

## Use API

### url
hostname/api

### required args
file : containing filename of the file

### optional args

lang : language code for tesseract ocr
renew : 1, if you want your file to be replaced with a new one. defult is 0 for False.
    