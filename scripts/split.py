import os
import glob
from utils.config import cfg
# from pdf2jpg import pdf2jpg
from pathlib import PurePath
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter

def pdf_remove (file, files_split):
    length = len(file)
    for i in range(length): 
        os.remove(files_split+"/{}".format(file[i])) #Remove existed pdf documents in folder.

def pdf_splitter(path, files_split):
    # fname = os.path.splitext(os.path.basename(path))[0]
    # 0: No results
    # 1: Files created
    # 2: Limit max numpages
    result = 0
    pdf = PdfFileReader(path)
    print("splitter")

    # if pdf.getNumPages() > cfg.FILES.MAX_NUMPAGES:
    #     result = 2
    # else:
    """
    Generating PDFs from splitter
    """
    try:
        if pdf.getNumPages() != None :
            for page in range(pdf.getNumPages()):
                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf.getPage(page))
                name_file = path.split("/")[-1].split(".pdf")[0]
                output_filename = files_split+'/'+name_file+'_{}.pdf'.format(page+1)

                with open(output_filename, 'wb') as out:
                    pdf_writer.write(out)
                print('Created: ' + name_file+'_{}.pdf'.format(page+1))
                result = 1
    except:
        result = 0
    
    return result


def img_splitter(path, files_split):
    # fname = os.path.splitext(os.path.basename(path))[0]
    result = 0
    # print("img splitter")
    images = convert_from_path(path, size=(600,900))

    for i in range(len(images)):
    # Save pages as images in the pdf
        images[i].save(files_split + '/page_'+ str(i) +'.jpg', 'JPEG')
        result = 1

    return result