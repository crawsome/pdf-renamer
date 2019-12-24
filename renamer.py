import re
import os
import PyPDF4
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path



print(
    'Welcome to PDFRenamer\n'
    '1. Put source PDFs into ./1_sources directory\n'
    '2. When the script runs, the OCRed text will be saved in ./3_textoutput/\n'
    '3. If there\'s a regex match, the files will be re-saved to ./4_pdfoutput/\n'
)

# test regex
regex ='^(CB-[\d]{4}-COL)$'

# phone number
# regex = '^\([0-9]{3}\)[0-9]{3}-[0-9]{4}$'
inputdir = './1_sources/'
imagedir = './2_imageoutput/'
textdir = './3_textoutput/'
outputdir = './4_pdfoutput/'

# get a list of everything in the directory to be RENAMED
original_doc_list = next(os.walk(inputdir))[2]
# 1: Read PDF
# 2. Create Image from PDF
# 3. Create Text from image
# 4. Regex text
# 5. Rename PDFs from step 1 to regex result

for filename in original_doc_list:
    out = open('{}{}.txt'.format(textdir, filename), 'w')
    out.seek(0)
    out.truncate()
    pdfFileObj = open('{}{}'.format(inputdir, filename), 'rb')
    pages = convert_from_path(pdfFileObj,500)
    no_of_pages = len(pages)
    for page in pages:
        page = pdfReader.getPage(page_no)
        page_content = page.extractText()
        page.save(filename, 'JPEG')
    out.close()
    pdfFileObj.close()

# get a list of the directory we are getting the new names from
text_doc_list = next(os.walk(textdir))[2]
print(text_doc_list)

for filename in text_doc_list:

    nextfile = textdir + filename
    print('processing ' + nextfile.strip('.txt'))
    with open(nextfile, 'r') as f:
        ourtext = str(f.read())
        f.close()
        #  fails here if there's nothing found
        try:
            nextname = re.findall(regex, ourtext)[0]
        except IndexError:
            print("No Matching Regex Found")
            quit()
        print('new name is: ' + nextname + '.pdf')
        proceed = input('Confirm? Y, N\n')
        if proceed == 'Y' or 'y':
            os.rename(inputdir + filename + '.pdf', outputdir + nextname + '.pdf')
        nextname = ''
