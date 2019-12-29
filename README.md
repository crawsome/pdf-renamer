# pdf-renamer
* Do you have many PDFs you need to rename? 
* Does the title exist in each of the PDFs?
* Can you create a [regex pattern](https://www.regexr.com) that can find the title?

##Backstory

A customer of mine had some data management software software that hashed the file names into some garbletygook, but the PDFs were simply renamed and moved into a folder. All the files were supposed to be **named to something inside it**. So once I figured out what the regex format was for the names, I wrote this script.

Inside the folder it would look like the ./1_sources directory in this project:

```
./1_sources/56md6asnm5.pdf
./1_sources/76ffy74cht.pdf
./1_sources/s5yhs5ys5y.pdf
```
And let's pretend all your purchase orders looks like this:
```
CB-###-COL
regex = ('(CB-[\d]{3,}-COL)')
```

But we would rather it look like this:

```
./4_pdfoutput
----CB-3415-COL.pdf
----CB-3715-COL.pdf
----CB-332535-COL.pdf
```



## High level explanation:
1. Goes into the ```./1_sources/```  folder for source PDFs
2. Converts all PDFs to images
3. Converts all images to text
4. Search through the text in the PDFs
5. Finds your desired title with your regex
6. For each file in your sources directory, copy a renamed file to output folder, each named according to your regex

##How to use
1. Put your desired PDFs in your ```./1_sources/``` directory
2. run ```renamer.py```
