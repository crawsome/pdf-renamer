# pdf-renamer
* Do you have many PDFs you need to rename? 
* Does the title exist in each of the PDFs?
* Can you create a [regex pattern](https://www.regexr.com) that can find the title?

##Backstory

A customer of mine had some data management software software that hashed the file names into some garbletygook, but the PDFs were simply renamed and moved into a folder. 

inside the folder it would look like the ./1_sources directory in this project:

```
./1_sources
----56md6asnm5.pdf
----76ffy74cht.pdf
----s5yhs5ys5y.pdf
```

So I wrote this script to: 
1. Go into the sources folder for source PDFs
2. Search through the text in the PDFs
3. Finds titles with your regex
4. For each file in your sources directory, copy a renamed file to output folder, each named according to your regex

