import os
from utils.config import cfg
from PyPDF2 import PdfFileReader, PdfFileWriter

def pdf_remove (file, files_split):
    length = len(file)
    for i in range(length): 
        os.remove(files_split+"/{}".format(file[i])) #Remove existed pdf documents in folder.
        # print("Deleted: {}".format(file[i]))

def pdf_splitter(path, files_split):
    # fname = os.path.splitext(os.path.basename(path))[0]
    # 0: No results
    # 1: Files created
    # 2: Limit max numpages
    result = 0
    pdf = PdfFileReader(path)

    if pdf.getNumPages() > cfg.FILES.MAX_NUMPAGES:
        result = 2
    else:
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