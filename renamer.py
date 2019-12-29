import re
import os
import shutil
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path, convert_from_bytes
import cProfile as cp

# Requires "poppler". https://stackoverflow.com/a/53960829
# poppler needs to be added to PATH

# Requires "pytesseract". https://github.com/UB-Mannheim/tesseract/wiki
# pytesseract needs to be added to PATH
def main():
    print(
        'Welcome to PDFRenamer\n'
        '1. Put source PDFs into ./1_sources directory\n'
        '2. When the script runs, the OCRed text will be saved in ./3_textoutput/\n'
        '3. If there\'s a regex match, the files will be re-saved to ./4_pdfoutput/\n'
    )

    # regex for searching for new file's name
    regex = re.compile('(CB-[\d]{3,}-COL)')
    # phone number
    # regex = '^\([0-9]{3}\)[0-9]{3}-[0-9]{4}$'

    inputdir = './1_sources/'
    imagedir = './2_imageoutput/'
    textdir = './3_textoutput/'
    outputdir = './4_pdfoutput/'

    # create all the directories above if they do not exist
    if not os.path.exists(inputdir):
        os.mkdir(inputdir)
        print('Please put source pdfs into {}, then rerun program'.format(inputdir))
        quit()
    if not os.path.exists(imagedir):
        os.mkdir(imagedir)
    if not os.path.exists(textdir):
        os.mkdir(textdir)
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)

    # get a list of everything in the directory to be RENAMED
    pdf_input_list = next(os.walk(inputdir))[2]
    # 1: Read PDF
    # 2. Create Image from PDF
    # 3. Create Text from image
    # 4. Regex text
    # 5. Rename PDFs from step 1 to regex result

    # 1: Read PDF
    # 2. Create Image from PDF
    for filename in pdf_input_list:
        out = open('{}{}.txt'.format(textdir, filename), 'w')
        image_file_path = '{}{}'.format(imagedir, filename.replace('.pdf', ''))
        pdf_file = open('{}{}'.format(inputdir, filename), 'rb')
        pdf_file_path = '{}{}'.format(inputdir, filename)
        # pages = convert_from_path(pdf_file, 500)
        pages = convert_from_path(pdf_file_path, 200)
        no_of_pages = len(pages)
        for index, page in enumerate(pages):
            img_path = image_file_path + '_page' + str(index + 1) + '.jpg'
            page.save(img_path, 'JPEG')
            text = str(pytesseract.image_to_string(Image.open(img_path)))
            # text = text.replace('-\n', '')
            out.write(text)
        out.close()

    # get a list of the directory we are getting the new names from
    text_doc_list = next(os.walk(textdir))[2]
    image_doc_list = next(os.walk(imagedir))[2]

    # If you need to make of every file name, use this one
    CONFIRM_EVERY_OPERATION = False

    ## OK Here's the potentially destructive part. By Default, it's safe to run and nothing deletes.
    # Change these vars to True to do what they imply
    DELETE_SOURCES_WHEN_FINISHED = False
    DELETE_TEXT_WHEN_FINISHED = False
    DELETE_IMAGES_WHEN_FINISHED = False


    # 4. read text, and 5. rename the PDFs
    for filename in text_doc_list:
        nextfile = textdir + filename
        print('processing ' + nextfile.strip('.txt'))
        with open(nextfile, 'r') as f:
            ourtext = str(f.read())
            f.close()
            #  fails here if there's nothing found
            try:
                nextname = re.findall(regex, ourtext)[0]
                print(nextname)
            except IndexError:
                print("No Matching Regex Found")
                quit()
            print('new name is: ' + nextname + '.pdf')
            proceed = ''
            if CONFIRM_EVERY_OPERATION:
                proceed = input('Confirm? Y, N\n')
            if (proceed == 'Y' or 'y') or CONFIRM_EVERY_OPERATION == False:
                in_pdf_name = inputdir + filename.replace('.txt', '')
                out_pdf_name = outputdir + nextname + '.pdf'
                # os.rename(in_pdf_name, out_pdf_name)
                shutil.copy(in_pdf_name, out_pdf_name)

            nextname = ''

    if DELETE_IMAGES_WHEN_FINISHED:
        for file in image_doc_list:
            os.remove(imagedir + file)
    if DELETE_TEXT_WHEN_FINISHED:
        for file in text_doc_list:
            os.remove(textdir + file)
    if DELETE_SOURCES_WHEN_FINISHED:
        for file in pdf_input_list:
            os.remove(inputdir + file)

if __name__ == '__main__':
    main()
