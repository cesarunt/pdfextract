import cv2
import re
import pytesseract
from pyzbar import pyzbar
from utils.config import cfg

pytesseract.pytesseract.tesseract_cmd = cfg.FILES.GLOBAL_TESSERACT

def qr_read(filename):
    result = None
    data = []
    measure = "H"
    file_qr = ""
    barcodes = []
    barcodeData = []

    # try:
    img = cv2.imread(filename, 0)
    if int(img.shape[1])>int(img.shape[0]):
        measure = "W"
        measure_h = "500px"
        measure_w = "740px"
        center_w = "0px"
    else:
        fw = float(int(img.shape[0]) / int(img.shape[1]))
        if fw > 2.0:
            # measure_w = str(int(float(img.shape[1])-50))+"px"
            measure_w = "420px"
            measure_h = "900px"
            center_w = "160px"
        elif fw > 1.75:
            measure_w = "480px"
            measure_h = "900px"
            center_w = "130px"
        else:
            measure_w = "640px"
            measure_h = "900px"
            center_w = "50px"

    detect = cv2.QRCodeDetector()
    _, box_coordinates, _ = detect.detectAndDecode(img)

    if box_coordinates is None:
        print('NO CODE QR')
        result = "TESS"
    else:
        barcodes = None
        print('ITS POSSIBLE CODE QR')
        # GET INFO FROM QR ICON
        barcodes = pyzbar.decode(img)
        
        if len(barcodes) > 0 :
            # loop over the detected barcodes
            for barcode in barcodes:
                barcodeText = str(barcode.data.decode("utf-8"))
                barcodeData = barcodeText.split('|')
            # print("barcodeData LEN", len(barcodeData))
            # print("barcodeData CONTENT", barcodeData)
            # IS FULL
            barcode_isok = 0
            if len(barcodeData)>8:
                barcode_isok = 1
            # GET BILL NUMBER
            n = 2
            if len(barcodeData[2].split('-')) > 1:
                barcode_fac = barcodeData[n]
            else:
                barcode_fac = barcodeData[n]+'-'+barcodeData[n+1]
                # n = n + 1

            data = {
                'is_full':  barcode_isok,
                'cia_ruc':  barcodeData[0],
                'cli_fac':  barcode_fac,
                'cli_igv':  barcodeData[n+1],
                'cli_tot':  barcodeData[n+2],
                'cli_dat':  barcodeData[n+3],
                'cli_nam':  barcodeData[n+4],
                'cli_ruc':  barcodeData[n+5],
                'measure':  measure,
                'measure_w':  measure_w,
                'measure_h':  measure_h,
                'center_w': center_w,
                'path':     ""
                }
            result = "OK"
        else:
            # CREATE QR IMAGE
            # image = cv2.imread(filename)
            img_crop = None
            box_coordinates = [box_coordinates[0].astype(int)]
            # print("box_coordinates len", len(box_coordinates))
            file_out = 'files/qr_upload/'+ str(filename).split('/')[-1].split('.j')[0]
            img_crop = img[box_coordinates[0][0][1]-15:box_coordinates[0][2][1]+15, box_coordinates[0][0][0]-15:box_coordinates[0][2][0]+15]
            # Scale
            data = []
            barcodes2 = []
            if len(img_crop)>0 and (img_crop.shape[1]>0):
                scale = 1
                width = int(img_crop.shape[1] * scale)
                height = int(img_crop.shape[0] * scale)
                img_crop = cv2.resize(img_crop, (width, height))
            
                # GET INFO FROM QR ICON 2
                barcodes2 = pyzbar.decode(img_crop)
                
                if len(barcodes2) > 0 :
                    file_qr = file_out + '_QR.png'
                    # print("FILE_QR", file_qr)
                    print('YES POSSIBLE CODE QR 2')
                    for barcode in barcodes2:
                        barcodeText2 = str(barcode.data.decode("utf-8"))
                        barcodeData2 = barcodeText2.split('|')
                    # IS FULL
                    barcode_isok = 0
                    if len(barcodeData2)>8:
                        barcode_isok = 1
                    # GET BILL NUMBER
                    n = 2
                    if len(barcodeData2[2].split('-')) > 1:
                        barcode_fac = barcodeData2[n]
                    else:
                        barcode_fac = barcodeData2[n]+'-'+barcodeData2[n+1]
                        # n = n + 1

                    data = {
                        'is_full':  barcode_isok,
                        'cia_ruc':  barcodeData2[0],
                        'cli_fac':  barcode_fac,
                        'cli_igv':  barcodeData2[n+1],
                        'cli_tot':  barcodeData2[n+2],
                        'cli_dat':  barcodeData2[n+3],
                        'cli_nam':  barcodeData2[n+4],
                        'cli_ruc':  barcodeData2[n+5],
                        'measure':  measure,
                        'measure_w':  measure_w,
                        'measure_h':  measure_h,
                        'center_w': center_w,
                        'path':     ""
                        }
                    result = "OK"
                else:
                    print("TESS")
                    result = "TESS"
            else:
                print("TESS")
                result = "TESS"
    
    if result == "TESS" :
        print("...GET DATA WITH TESSERACT")
        text = pytesseract.image_to_string(img, lang='spa', config='--psm 6')
        # print(text)
        res_rucs = None
        patterns_cli_igv = ["GV: ", "6V :", "IGV:", "18%", "18.00%"]
        patterns_cli_tot = ["IMPORTE TOTAL" , "TOTAL ", "TOTAL:"]
        patterns_cli_fec = []
        data_cia_ruc = ""
        data_cli_fac = ""
        data_cli_igv = ""
        data_cli_tot = ""
        data_cli_fec = ""
        data_cli_ruc = ""

        # FIND RUC
        res_rucs = re.findall("2\d{10,}", text)
        len_ruc = len(res_rucs)
        if len_ruc>0:
            if len_ruc == 1:
                data_cia_ruc = res_rucs[0]
            elif len_ruc>1:
                data_cia_ruc = res_rucs[0]
                data_cli_ruc = res_rucs[1]
        else:
            res_rucs = re.findall(r"RUC2[0-9]+(?:-[0-9]+)", text)
            if len(res_rucs)>0:
                data_cia_ruc = str(res_rucs[0][3:]).split(" ")[0]
        # FIND BILL NUMBER
        res_bill_1 = re.search("[F,E]\d{3}", text)
        if res_bill_1 != None:
            data_cli_fac = str(text[res_bill_1.start(0):]).split("\n")[0]
        else:
            match = False
            res_bill_2 = re.search(" A\w{5,15}", text)
            if res_bill_2 != None:
                # res_bill_ = str(text[res_bill_2.start(0):]).split(" ")[0]
                res_bill_ = str(res_bill_2.group(0))[1:].split(" ")[0]
                match = re.search(r'[a-zA-Z]+', res_bill_) and re.search(r'[0-9]+', res_bill_)
                if match:
                    data_cli_fac = res_bill_
        # FIND TOTAL
        for pattern in patterns_cli_tot :
            patt = re.search(rf"\b{pattern}", text, re.IGNORECASE)
            if patt != None :
                obj = str(text[patt.start(0):]).split("\n")[0].upper()
                if len(obj)>0:
                    data_cli_tot = str(obj.split(pattern)[-1]).replace(" ","").replace(":","").replace("S","").replace("$","").replace("/","").replace("%","").replace("-","").replace("I","").replace("PAGADO","").replace("FACTURA","").replace("PAGAR","").replace("Y","")
                    break
        # FIND IGV
        for pattern in patterns_cli_igv :
            patt = re.search(rf"{pattern}", text, re.IGNORECASE)
            if patt != None :
                obj = str(text[patt.start(0):]).split("\n")[0].upper()
                if len(obj)>0:
                    data_cli_igv = str(obj.split(pattern)[-1]).replace(" ",'').replace(":",'').replace("S",'').replace("$",'').replace("/",'').replace("%",'').replace("-",'').replace("I","").replace("PAGADO","").replace("FACTURA","").replace("PAGAR","").replace("Y","")
                    break
        data_cli_tot = str(data_cli_tot).replace('—','')
        # FIND DATE
        patterns_cli_fec.append(re.search(r'\d{2}/\d{2}/\d{4}', text))
        patterns_cli_fec.append(re.search(r'\d{2}-\d{2}-\d{4}', text))
        patterns_cli_fec.append(re.search(r'\d{4}/\d{2}/\d{2}', text))
        patterns_cli_fec.append(re.search(r'\d{4}-\d{2}-\d{2}', text))
        for pattern in patterns_cli_fec :
            if pattern != None:
                data_cli_fec = pattern.group(0)
                break
        
        res_data = [data_cia_ruc, data_cli_fac, data_cli_igv, data_cli_tot, data_cli_fec, data_cli_ruc]
        res_len = len([x for x in res_data if x != ""])
        # IS FULL
        barcode_isok = 0
        if res_len>4:
            barcode_isok = 2
        
        data = {
                'is_full':  barcode_isok,
                'cia_ruc':  data_cia_ruc,
                'cli_fac':  data_cli_fac,
                'cli_igv':  data_cli_igv,
                'cli_tot':  data_cli_tot,
                'cli_dat':  data_cli_fec,
                'cli_ruc':  data_cli_ruc,
                'measure':  measure,
                'measure_w':  measure_w,
                'measure_h':  measure_h,
                'center_w': center_w,
                'path':     file_qr
                }
        result = "OK"

    # except Exception as e:
    #     print(e)
    #     return
    
    return result, data
