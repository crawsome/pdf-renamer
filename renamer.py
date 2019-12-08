import re
import os
import PyPDF4

# our beautiful regex (for my client)
regex = '^(PPA[-, ]*[\d]{2}-\d{3,5})$'

# phone number
# regex = '^\([0-9]{3}\)[0-9]{3}-[0-9]{4}$'
inputdir = './1_sources/'
textdir = './2_textoutput/'
outputdir = './3_output/'

# get a list of everything in the directory to be RENAMED
original_doc_list = next(os.walk(inputdir))[2]
print(original_doc_list)
# 1: Read PDF in as text

for filename in original_doc_list:
    out = open('{}{}.txt'.format(textdir,filename), 'w')
    out.seek(0)
    out.truncate()
    pdfFileObj = open('{}{}'.format(inputdir,filename), 'rb')
    pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
    no_of_pages = pdfReader.getNumPages()
    print(no_of_pages)
    for page_no in range(no_of_pages):
        page = pdfReader.getPage(page_no)
        for i in range(4):
            page.rotateCounterClockwise(90)
            page_content = page.extractText()
            out.write(page_content)
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
        # it fails here if there's nothing found
        nextname = re.findall(regex, ourtext)[0]
        print('new name is: ' + nextname + '.pdf')
        proceed = input('Confirm? Y, N\n')
        if proceed == 'Y' or 'y':
            os.rename(inputdir + filename + '.pdf', outputdir + nextname + '.pdf')
        nextname = ''

