import re
import os
import shutil
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

# Windows Issues:
# 1. Requires "poppler". https://stackoverflow.com/a/53960829. poppler also needs to be added to PATH
# 2. Requires "pytesseract". https://github.com/UB-Mannheim/tesseract/wiki. pytesseract also needs to be added to PATH

# Global Vars:

# 500dpi = around 6 seconds per page, 250 = 3 seconds, 100 <1second per PDF.
# # Anything below 100 is not very reliable.
DPI_LEVEL = 100

# If you need to make sure of every file name, use this one
CONFIRM_EVERY_OPERATION = False

# Delete original source PDFs when done
DELETE_SOURCES = False

# Delete text output of each PDF
DELETE_TEXT = False

# Delete image copies of PDFs. Recommended to leave this at True, because the image copies waste space
DELETE_IMAGES = True

# regex for searching for file's name within source documents. Works with included example docs. Replace with your own.
OUR_REGEX = re.compile('(CB-[\d]{3,}-COL)')

PDF_INPUT_DIR = './1_sources/'
IMAGE_DIR = './2_imageoutput/'
TEXT_DIR = './3_textoutput/'
PDF_OUTPUT_DIR = './4_pdfoutput/'




def pdf_to_jpg(pdffile, outfile):
    pass

def regex_find(text, regex):
    pass

def jpg_to_text(pdffile, outfile):
    pass


# verifies or create all the included directories in args list if they do not exist
def check_or_create_directories(*args):
    for directory in args:
        print('created dir: ' + str(directory))
        if not os.path.exists(directory):
            os.mkdir(directory)

def delete_directories(folderlist, doclist, deletelist):
    for documentdir, documentname, deletebool in zip(folderlist, doclist, deletelist):
        if deletebool:
            try:
                nextfile = str(documentdir) + str(documentname[0])
                print('attempting to remove' + nextfile)
                os.remove(nextfile)
            except IndexError:
                print('{} Empty, nothing to remove'.format(documentdir))

def main():
    print(
        'Welcome to PDFRenamer\n'
        '1. Put source PDFs into ./1_sources directory\n'
        '2. When the script runs, the OCRed text will be saved in ./3_textoutput/\n'
        '3. If there\'s a regex match, the files will be re-saved to ./4_pdfoutput/\n'
    )

    check_or_create_directories(PDF_INPUT_DIR, IMAGE_DIR, TEXT_DIR, PDF_OUTPUT_DIR)

    # get a list of everything in the directory to be RENAMED
    pdf_doc_list = next(os.walk(PDF_INPUT_DIR))[2]

    # 1: Read PDF
    for filename in pdf_doc_list:
        textfilepath = '{}{}'.format(TEXT_DIR, filename.replace('.pdf', '.txt'))

        text_file = open(textfilepath, 'w')

        imagefile = '{}{}'.format(IMAGE_DIR, filename.replace('.pdf', ''))

        pdffilepath = '{}{}'.format(PDF_INPUT_DIR, filename)

        pages = convert_from_path(pdffilepath, DPI_LEVEL)

        # 2. Create Images from PDFs
        for index, page in enumerate(pages):
            img_path = imagefile + '_page' + str(index + 1) + '.jpg'
            page.save(img_path, 'JPEG')
            text = str(pytesseract.image_to_string(Image.open(img_path)))
            text_file.write(text)
        text_file.close()

    image_doc_list = next(os.walk(IMAGE_DIR))[2]
    text_doc_list = next(os.walk(TEXT_DIR))[2]

    nextname = ''
    # 3. Read text, 4. Find names, 5. Copy and rename source pdfs.
    for filename in text_doc_list:
        nextfile = TEXT_DIR + filename
        print('processing ' + nextfile.strip('.txt'))
        with open(nextfile, 'r') as f:
            ourtext = str(f.read())
            f.close()
            try:
                nextname = re.findall(OUR_REGEX, ourtext)[0]
                print(nextname)
            except IndexError:
                print("No Matching Regex Found")
                quit()
            print('new name is: ' + nextname + '.pdf')
            proceed = ''
            if CONFIRM_EVERY_OPERATION:
                proceed = input('Confirm? Y, N\n')
            if (proceed == 'Y' or 'y') or not CONFIRM_EVERY_OPERATION:
                in_pdf_name = PDF_INPUT_DIR + filename.replace('.txt', '')
                out_pdf_name = PDF_OUTPUT_DIR + nextname + '.pdf'
                shutil.copy(in_pdf_name, out_pdf_name)



    delete_directories([PDF_INPUT_DIR, IMAGE_DIR, TEXT_DIR], [pdf_doc_list, image_doc_list, text_doc_list],
                       [DELETE_SOURCES, DELETE_IMAGES, DELETE_TEXT])


if __name__ == '__main__':
    main()
