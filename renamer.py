import re
import os
import shutil
from PIL import Image
import pytesseract
from pdf2image import convert_from_path, convert_from_bytes

# Windows Issues:
# 1. Requires "poppler". https://stackoverflow.com/a/53960829. poppler also needs to be added to PATH
# 2. Requires "pytesseract". https://github.com/UB-Mannheim/tesseract/wiki. pytesseract also needs to be added to PATH

# Global Vars:

# 500dpi = around 6 seconds per page, 250 = 3 seconds, 100 <1second per PDF.
# # Anything below 100 is not very reliable.
DPI_LEVEL = 100

# If you need to make sure of every file name, use this one
CONFIRM_EVERY_OPERATION = False

# By Default, it's safe to run and no source deletes.
# Change these following vars to True to do what they imply

# Delete original source PDFs when done
DELETE_SOURCES_WHEN_FINISHED = False

# Delete text output of each PDF
DELETE_TEXT_WHEN_FINISHED = False

# Delete image copies of PDFs. Recommended to leave this at True, because the image copies waste space
DELETE_IMAGES_WHEN_FINISHED = True

# regex for searching for new file's name
OUR_REGEX = re.compile('(CB-[\d]{3,}-COL)')


def main():
    print(
        'Welcome to PDFRenamer\n'
        '1. Put source PDFs into ./1_sources directory\n'
        '2. When the script runs, the OCRed text will be saved in ./3_textoutput/\n'
        '3. If there\'s a regex match, the files will be re-saved to ./4_pdfoutput/\n'
    )

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

    for filename in pdf_input_list:
        out = open('{}{}.txt'.format(textdir, filename), 'w')
        image_file_path = '{}{}'.format(imagedir, filename.replace('.pdf', ''))
        pdf_file_path = '{}{}'.format(inputdir, filename)
        pages = convert_from_path(pdf_file_path, DPI_LEVEL)

        # 2. Create Image from PDF
        for index, page in enumerate(pages):
            img_path = image_file_path + '_page' + str(index + 1) + '.jpg'
            page.save(img_path, 'JPEG')
            text = str(pytesseract.image_to_string(Image.open(img_path)))
            out.write(text)
        out.close()

    # get a list of the directory we are getting the new names from
    text_doc_list = next(os.walk(textdir))[2]
    image_doc_list = next(os.walk(imagedir))[2]

    # 4. read text, 5. find names, 6. copy and rename source pdfs.
    for filename in text_doc_list:
        nextfile = textdir + filename
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
            if (proceed == 'Y' or 'y') or CONFIRM_EVERY_OPERATION == False:
                in_pdf_name = inputdir + filename.replace('.txt', '')
                out_pdf_name = outputdir + nextname + '.pdf'
                shutil.copy(in_pdf_name, out_pdf_name)

            nextname = ''

    if DELETE_IMAGES_WHEN_FINISHED:
        for file in image_doc_list:
            os.remove(imagedir + file)
    if DELETE_TEXT_WHEN_FINISHED:
        for file in text_doc_list:
            os.remove(textdir + file)
    if DELETE_SOURCES_WHEN_FINISHED:  # permission errors sometimes
        for file in pdf_input_list:
            os.remove(inputdir + file)


if __name__ == '__main__':
    main()
