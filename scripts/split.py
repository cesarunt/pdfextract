import os
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
    pdf_npages = pdf.getNumPages()

    # if pdf.getNumPages() > cfg.FILES.MAX_NUMPAGES:
    #     result = 2
    # else:
    """
    Generating PDFs from splitter
    """
    try:
        if pdf_npages != None :
            for page in range(pdf.getNumPages()):
                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf.getPage(page))
                name_file = path.split("/")[-1].split(".pdf")[0]
                output_filename = files_split+'/'+name_file+'_{}.pdf'.format(page+1)
                with open(output_filename, 'wb') as out:
                    pdf_writer.write(out)
                # print('Created: ' + name_file+'_{}.pdf'.format(page+1))
            print('Created ' + str(pdf_npages) + ' pdfs, to ' + name_file +'.pdf')
            result = 1
    except:
        result = 0
    
    return result, pdf_npages


def img_splitter(path, files_split, pdf_info_id):
    # fname = os.path.splitext(os.path.basename(path))[0]
    result = 0
    images = convert_from_path(path, size=(700,1000))
    img_npages = len(images)
    # Create directory for each pdf
    # dir_pdf = files_split+"/"+str(pdf_info_id)
    # try:
    #     os.mkdir(dir_pdf)
    #     print("mkdir-OK")
    # except OSError:
    #     print("La creación del directorio %s falló" % dir_pdf)
    # else:
    #     print("Se ha creado el directorio: %s " % dir_pdf)

    for i in range(img_npages):
    # Save pages as images in the pdf
        images[i].save(files_split + '/' + str(pdf_info_id) + 'page_'+ str(i) +'.jpg', 'JPEG')
        result = 1

    return result, img_npages