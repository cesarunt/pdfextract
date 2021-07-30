import os
from PyPDF2 import PdfFileReader, PdfFileWriter

def pdf_remove (file):
    length = len(file)
    for i in range(length): 
        os.remove("split/{}".format(file[i])) #Remove existed pdf documents in folder.
        print("Deleted: ../split/{}".format(file[i]))

def pdf_splitter(path):
    # fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output_filename = 'split/'+path.split("/")[-1].split(".pdf")[0]+'_{}.pdf'.format(page+1)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
        print('Created: {}'.format(output_filename))