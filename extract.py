# Extract PDF
import os
from scripts.split import pdf_remove, pdf_splitter
from scripts.process import pdf_process

if __name__ == '__main__':

    # 1. Split PDF
    # ============
    # list of 20 PDFs files
    # path = "input/1._Arias-Munoz(2019).pdf"
    # path = "input/2._Zarraga-Cano-Molina-Morejon(2018).pdf"  # FILE IMAGE TITLE
    path = "input/3._Salazar-Yepez-Cabrera-Vallejo(2016).pdf"
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
    print("\n------------------- START SPLIT PROCESS -------------------")
    pdf_remove(fname)       # Call pdf remove function
    pdf_splitter(path)      # Call pdf splitter function

    # 2. Process PDF
    # ==============
    print("\n------------------ START EXTRACT PROCESS ------------------")
    pdf_process()           # Call pdf process function