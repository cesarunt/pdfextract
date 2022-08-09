import os
from utils.config import cfg
# from pdf2jpg import pdf2jpg
from pathlib import PurePath
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter


def pdf_getNpages(path):
    pdf = PdfFileReader(path)
    pdf_npages = pdf.getNumPages()
    return pdf_npages


def pdf_remove(file, files_split):
    length = len(file)
    for i in range(length): 
        os.remove(files_split+"/{}".format(file[i])) #Remove existed pdf documents in folder.

def pdf_splitter(path, files_split, pdf_info_id):
    # fname = os.path.splitext(os.path.basename(path))[0]
    # 0: No results
    # 1: Files created
    # 2: Limit max numpages
    result = 0
    pdf = PdfFileReader(path)
    pdf_npages = pdf.getNumPages()
    """
    Generating PDFs from splitter
    """
    try:
        if pdf_npages != None :
            for page in range(pdf.getNumPages()):
                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf.getPage(page))
                # name_file = path.split("/")[-1].split(".pdf")[0]
                output_filename   = files_split+'/'+str(pdf_info_id)+'page'+'_{}.pdf'.format(str(page+1))
                # output_filename = files_split+'/'+pdf_info_id+"page"+'_{}.pdf'.format(page+1)
                with open(output_filename, 'wb') as out:
                    pdf_writer.write(out)
                # print('Created: ' + name_file+'_{}.pdf'.format(page+1))
            print('Created ' + str(pdf_npages) + ' pdfs')
            result = 1
    except:
        result = 0
    
    return result, pdf_npages


def img_remove(file, files_split):
    length = len(file)
    for i in range(length): 
        os.remove(files_split+"/{}".format(file[i])) #Remove existed pdf documents in folder.

def img_splitter(path, files_split, pdf_info_id):
    result = 0
    images = convert_from_path(path, size=(700,1000))
    img_npages = len(images)

    # Save pages as images in the pdf
    for i in range(img_npages):
        images[i].save(files_split + '/' + str(pdf_info_id) + 'page_'+ str(i) +'.jpg', 'JPEG')
        result = 1

    return result, img_npages