import os
from utils.config import cfg
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader, PdfFileWriter


def pdf_getNpages(path):
    pdf_npages = 0
    pdf = PdfFileReader(path)
    try:
        pdf_npages = pdf.getNumPages()
    except:
        pdf_npages = 0
    return pdf_npages

def pdf_splitter(path, files_split, pdf_info_id, pdfs):
    # 0: No results
    # 1: Files created
    result = 0
    pdf = PdfFileReader(path)
    try:
        pdf_npages = pdf.getNumPages()
        if len(pdfs)>0:
            list_pages = pdfs[str(pdf_info_id)]
            pdf_npages = len(list_pages)
        else:
            list_pages = range(pdf_npages)
        # try:
        """
        Generating PDFs from splitter
        """
        if pdf_npages != None and pdf_npages > 0 :
            # Save pages as images in the pdf
            for page in list_pages:
                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf.getPage(page))
                output_filename = files_split+'/'+str(pdf_info_id)+'page'+'_{}.pdf'.format(str(page+1))
                pdf_output = open(output_filename, 'wb')
                pdf_writer.write(pdf_output)
                pdf_output.close()
            print('Created ' + str(pdf_npages) + ' pdfs')
            result = 1
    except:
        pdf_npages = 0
        result = -1
    
    return result, pdf_npages

def split_thumb(path, files_split, pdf_info_id):
    result = 0
    images = convert_from_path(path, dpi=200, size=(100,160))
    img_npages = len(images)
    # Save pages as thumbnail
    for i in range(img_npages):
        images[i].save(files_split + '/' + str(pdf_info_id) + 'page_'+ str(i) +'.jpg',  format='JPEG', subsampling=0, quality=80)
        result = 1

    return result

def split_img(path, files_split, pdf_info_id):
    result = 0
    images = convert_from_path(path, dpi=300, size=(640,820))
    img_npages = len(images)
    # Save pages as thumbnail
    for i in range(img_npages):
        images[i].save(files_split + '/' + str(pdf_info_id) + 'page_'+ str(i) +'.jpg',  format='JPEG', subsampling=0, quality=100)
        result = 1

    return result

def split_img_qr(path, files_split):
    result = False
    pdf_reader = PdfFileReader(path)
    box = pdf_reader.pages[0].mediaBox
    pdf_width = box.getWidth()
    pdf_height = box.getHeight()
    image = convert_from_path(path, dpi=300, size=(pdf_width, pdf_height))
    filename = files_split + '/' + str(path.split("/")[-1]).split(".")[0] + '.jpg'
    # for i in range(img_npages):
    if image:
        image[0].save(filename,  format='JPEG', subsampling=0, quality=100)
        filename = str(filename).split("/")[-1]
        result = True

    return result, filename