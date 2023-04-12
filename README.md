# Text Extraction Api Services - TExASe

![](static/default-logo.png "It-Sr-NER")

#### TExASe is a flask application for document processing, namely Extraction of text from it (with application of OCR if necessary). 
#### Most of the provided services require a file as an input.

#### In addition to this, TExASe offers support for repositories, through a set of services and functions that read document metadata, generate citation strings, and most notably, generate cover pages for the documents using the supplied metadata, configuration, html, css files and images.


# List of services
### Basic services
- **extract** - Extracts text from the provided file using [tika-python](https://pypi.org/project/tika/) port for [apache tika](https://tika.apache.org/). It requires only a file (with readable content) and returns text.


- **ocr** - Performs OCR on PDF-s and image-files not containing readable text. 
  Image processing in done using [tesseract-ocr](https://github.com/tesseract-ocr/tesseract) via [pytesseract](https://pypi.org/project/pytesseract/) and [Pillow](https://pillow.readthedocs.io/en/stable/), while pdf processing is done using [ocrmypdf](https://github.com/ocrmypdf/OCRmyPDF), also based on [tesseract-ocr](https://github.com/tesseract-ocr/tesseract).
  This service accept optional language code along the required file and returns a new, readable, file as a result.


- **ocr_and_extract** - First performs OCR on unreadable files to make them readable, and then extracts the text from them.
  It returns an HTML containing extracted text, as well as a base64 string of a new file (if OCR was performed).


- **renew** - Only works with file_paths. It OCR-s a file on the provided path and then replace it with a new version.
  
### Repository services
- **add_cover** - Adds a cover page to a supplied PDF file. The cover page will contain information about supplied (**repo** param) or default repository, as well as metadata if appropriate item **id** for targeted repository was submitted.
Cover page is created using [pdfkit](https://pypi.org/project/pdfkit/) via [wkhtmltopdf](https://wkhtmltopdf.org/), and PDF pages are added or subtracted using [PyPDF2](https://pypi.org/project/PyPDF2/).


- **remove_cover** - This will remove the cover page of a supplied pdf, if it has one, using [PyPDF2](https://pypi.org/project/PyPDF2/).


- **remove_all_covers** - This will trigger **remove_cover** for all pdfs on a supplied **path**.


- **metadata** - This will return metadata for a file, if you supply it with an appropriate **id** for a given of default **repo**.


- **citation** - This works just like the **metadata** service, except it returns a citation string for the item instead of the metadata.




## Use GUI
Simply, on the left, pick a file and click process. The result will appear on the right.

Optionally, if you want a more precise OCR, input a (supported) language code for tesseract bellow.

Current GUI supports only **ocr_and_extract** service.

## Use API

### url
hostname/api/**service_name**

### required arg
**file** : containing filename of a posted file.

### optional args

Optional args are definied for each service in the [config.json](config.json) file. 
For example **ocr** service accepts **lang** (language code for tesseract ocr) parameter.



# Options

Some of the options are configured in the [config.json](config.json) file. 
These include:

**tesseract** : tesseract service options, including a list of default languages to be used in OCR, path to tesseract service, as well as a list of applicable extensions.

**log** : string, file location of a writable log file. If the file is specified and writable, all requests will be logged in it.

**wkhtmltopdf_path** : string, path to executables for **wkhtmltopdf**, required for creation of PDFs from HTML strings.

**default_repo** : string, name of the default repository (folder with required files in the **repos** dir of this project). This will affect creation of the cover pages for submitted PDFs.

**redis** : redis server options. If **on** is set to **1**, all requests will go through a redis queue on specified **url** and **port**. Redis is only available for services that do not return a value.

**services** a list of available services, and their respected parameter definitions.

# Requirements
    sudo apt-get install python3-dev libxml2-dev libxslt1-dev tesseract-ocr ghostscript

for ubuntu and

    pip install flask redis rq pdfkit tika ocrmypdf pytesseract Pillow

from pip.