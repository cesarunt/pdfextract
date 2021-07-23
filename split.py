import os
from PyPDF2 import PdfFileReader, PdfFileWriter

def pdf_remove (length):
    for i in range(length): 
        os.remove("split/{}".format(fname[i])) #Remove existed pdf documents in folder.
        print("Deleted: ../split/{}".format(fname[i]))

def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output_filename = 'split/'+path.split("/")[-1].split(".pdf")[0]+'_{}.pdf'.format(page+1)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
        print('Created: {}'.format(output_filename))

if __name__ == '__main__':
    path = "input/1._Arias-Munoz(2019).pdf"
    # path = "input/2._Zarraga-Cano-Molina-Morejon(2018).pdf"  # FILE IMAGE TITLE
    # path = "input/3._Salazar-Yepez-Cabrera-Vallejo(2016).pdf"
    # path = "input/4._Morillo-Moreno-(2016).pdf"
    # path = 'input/5._Mejias-Acosta-(2018).pdf'          # Falta condicion UNIVERSIDAD
    # path = "input/6._Villalobos-Fernandez(2016).pdf"
    # path = "input/7._BurgosChavez-Morocho(2020).pdf"  # FILE NOT DECRYPTED
    # path = "input/8._CrispinAranda-ToreroSolano(2020).pdf"
    # path = "input/9._SotomayorChambilla(2016).pdf"
    # path = "input/10._GangaContreras-AlarcónHenríquez(2019).pdf"
    # path = "input/1._Suciptawati.pdf"
    # path = "input/2._Balinado-Pasetyo.pdf"
    # path = "input/3._Setiari.pdf"
    # path = "input/4._Hisam.pdf"
    # path = "input/5._Ok.pdf"
    # path = "input/6._Kwok.pdf"
    # path = "input/7._Surahman.pdf"
    # path = "input/8._Akroush.pdf"
    # path = "input/9._Rashid.pdf"
    # path = "input/10._Thanh.pdf"

    fname = os.listdir('split/') #fname: List contain pdf documents names in folder
    length = len(fname) #Retrieve List fname Length.

    #call pdf remove function
    pdf_remove(length) 
    #call pdf splitter function
    pdf_splitter(path)