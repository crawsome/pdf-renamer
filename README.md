# pdf-renamer
* Do you have many PDFs you need to rename? 
* Does the title exist in each of the PDFs?
* Can you create a [regex pattern](https://www.regexr.com) that can find the title?

## Backstory

A customer of mine had some really crappy data management software software that hashed the file names into some garbletygook, and tossed them into a deep directory. 

The software company went out of business, and the PDFs seemed lost. 

Sadly, but luckily, the PDFs were simply renamed and moved into a folder. 

All the files were supposed to be **named to something inside each file**. 

So once I figured out what the regex format was for the names, I wrote this script.

Inside the folder it would look like the ./1_sources directory in this project:

```
./docfolder/
----56md6asnm5.pdf <--- order number CB-3415-COL shown inside the document
----76ffy74cht.pdf <--- order number CB-3715-COL shown inside the document
----s5yhs5ys5y.pdf <--- order number CB-332535-COL shown inside the document
```
We figure out a regex that matches the title format:
```
CB-###-COL
regex = ('(CB-[\d]{3,}-COL)')
```

But we would rather it look like this:

```
./docfolder/
----CB-3415-COL.pdf
----CB-3715-COL.pdf
----CB-332535-COL.pdf
```



## High level explanation:
1. Goes into the ```./1_sources/```  folder for source PDFs
2. Converts all PDFs to images using ```pdf2image``` which uses the ```PIL``` (pillow library), and drops them into the ```./2_imageoutput/``` directory.
3. Converts all images to text using ```pytesseract```, and drops them in the ```/3_textoutput/``` directory.
4. Search through the text in the PDFs using ```re``` (regex library)
5. Finds your desired title with your regex
6. Creates renamed files in the ```./4_pdfoutput/'``` firectory each named according to your regex.

## How to use
It is **highly recommended** you run the script with a copy sample of subset of your source files, then run with a copy just in case there's any destructive behavior. 

1. Put your desired PDFs in your ```./1_sources/``` directory.
2. Optionally set flags in script:
   2. DPI_LEVEL (default is 100)
   2. CONFIRM_EVERY_OPERATION (default is False)
   2. DELETE_SOURCES_WHEN_FINISHED (default is False)
   2. DELETE_TEXT_WHEN_FINISHED (default is False)
   2. DELETE_IMAGES_WHEN_FINISHED (default is False)
3. run ```renamer.py```

More features / modularization to come soon!
