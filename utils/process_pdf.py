from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO, StringIO

# PDF to text function
def convert_pdf_to_text(path):
    manager = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    layout = LAParams(all_texts=True)
    device = TextConverter(manager, retstr, codec = codec, laparams=layout)
    filepath = open(path, 'rb')
    interpreter = PDFPageInterpreter(manager, device)

    for page in PDFPage.get_pages(filepath, check_extractable=True):
        interpreter.process_page(page)
        text = retstr.getvalue()
    
    filepath.close()
    device.close()
    retstr.close()
    return text

# PDF to html-text function
def convert_pdf_to_html(path):
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    codec = 'utf-8'
    laparams = LAParams(all_texts=True)
    device = HTMLConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
    filepath = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(filepath, pagenos, maxpages = maxpages, password = password, caching = caching, check_extractable = True):
        # interpreter.process_page(page)
        try:
            interpreter.process_page(page)
        except:
            continue

    filepath.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str
