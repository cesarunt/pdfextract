import os
from flask import Flask, render_template, request, redirect, make_response, jsonify, send_file
from utils.config import cfg
from utils.handle_files import allowed_file, allowed_file_filesize, get_viewProcess_CPU
from werkzeug.utils import secure_filename
from scripts.split import pdf_remove, pdf_splitter
from scripts.process import pdf_process

app = Flask(__name__)

app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['MAX_CONTENT_LENGTH'] = cfg.FILES.MAX_CONTENT_LENGTH 
app.config['UPLOAD_EXTENSIONS']  = cfg.FILES.UPLOAD_EXTENSIONS
app.config['SINGLE_UPLOAD']      = cfg.FILES.SINGLE_UPLOAD
app.config['SINGLE_SPLIT']       = cfg.FILES.SINGLE_SPLIT
app.config['SINGLE_OUTPUT']      = cfg.FILES.SINGLE_OUTPUT
app.config['SINGLE_FORWEB']      = cfg.FILES.SINGLE_FORWEB
app.config['MULTIPLE_UPLOAD']    = cfg.FILES.MULTIPLE_UPLOAD
app.config['MULTIPLE_SPLIT']     = cfg.FILES.MULTIPLE_SPLIT
app.config['MULTIPLE_OUTPUT']    = cfg.FILES.MULTIPLE_OUTPUT
app.config['MULTIPLE_FORWEB']    = cfg.FILES.MULTIPLE_FORWEB

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Index
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/extract_one')
def extract_one():
    return render_template('extract_one.html')

@app.route('/extract_mul')
def extract_mul():
    return render_template('extract_mul.html')

@app.route('/report')
def report():
    return render_template('report.html')

# ----------------------------------- PDF EXTRACT ONE -----------------------------------
@app.route('/extract_one', methods=['POST'])
def extract_one_load():
    global file_pdf
    active_show = "active show"
    # _analytic = request.form.get('analytic')

    if request.method == "POST":
        # # Code for multiple pdfs
        # if 'files[]' not in request.files:
        #     print('No file part')
        #     return redirect(request.url)

        # files = request.files.getlist('files[]')

        # for file in files:
        #     if file and allowed_file(file.filename):
        #         filename = secure_filename(file.filename)
        #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # print('File(s) successfully uploaded')
        # return redirect('/')

        # Code for One pdf
        if "filesize" in request.cookies:
            if not allowed_file_filesize(request.cookies["filesize"], app.config["MAX_CONTENT_LENGTH"]):
                print("Filesize exceeded maximum limit")
                return redirect(request.url)
            file = request.files["file"]
            filesize = request.cookies.get("filesize")

            if file.filename == "":
                print("No filename")
                return redirect(request.url)
            if int(filesize) > 0 :
                res = make_response(jsonify({"message": f"El PDF fue cargado con éxito."}), 200)
                print("File uploaded")
                upload = True
            if allowed_file(file.filename, app.config["UPLOAD_EXTENSIONS"]):
                filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config["UPLOAD_PATH_UP"], filename))
                file.save(os.path.join(app.config["SINGLE_UPLOAD"], filename))
                file_pdf = filename
                print("File saved")
                if (upload == True):
                    return res
            else:
                print("That file extension is not allowed")
                return redirect(request.url)

@app.route("/action_extract_one", methods=["GET", "POST"])
def action_extract_one():
    active_show = "active show"
    result_process = False

    if request.method == "POST":
        global file_pdf, resultText, file_show #resultAlert
        (resultText, file_show) = ("", "")

        # Verify if posible to process
        if get_viewProcess_CPU() is True :
            path = os.path.join(app.config['SINGLE_UPLOAD'],file_pdf)
            fname = os.listdir(app.config['SINGLE_SPLIT']) #fname: List contain pdf documents names in folder
            # 1. SPLIT PDF
            # print("\n------------------- START SPLIT PROCESS -------------------")
            pdf_remove(fname)       # Call pdf remove function
            pdf_splitter(path)      # Call pdf splitter function
            # 2. Process PDF
            # print("\n------------------ START EXTRACT PROCESS ------------------")
            result_process = pdf_process()           # Call pdf process function
            print("Out web: " + app.config['SINGLE_FORWEB'])
            if result_process == True :
                # mask_imageOut = os.path.join(app.config['PATH_OUT_FORWEB'], (sub+file_image))
                file_show = file_pdf.split(".pdf")[0]
                # read the background from "background.txt" o "background.docx"
                resultText = app.config['SINGLE_FORWEB']+'/background.docx'
            # else:
            #     resultAlert = "No fue posible procesar la imagen"
        else:
            file_show = "None"
            # resultAlert = "El servidor está procesando, debe esperar un momento."
    
    print("Res: " + str(resultText))
    return render_template('extract_one.html', resultText=resultText, file_show=file_show)

@app.route("/close_extract_one/<source>")
def close_extract_one(source):
    url = "/" + source
    return redirect(url)

@app.route("/save_extract_one", methods=["POST"])
def save_extract_one():
    if request.method == "POST":
        down_image = request.form.get('down_image')
        
    return send_file(down_image, as_attachment=True)


# ----------------------------------- PDF EXTRACT MULTIPLE -----------------------------------
@app.route('/extract_mul', methods=['POST'])
def extract_mul_load():
    global file_pdf
    upload = False
    # _analytic = request.form.get('analytic')

    if request.method == "POST":
        # Code for multiple pdfs
        if 'files[]' not in request.files:
            print('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            print("Name: " + file.filename)
            if file and allowed_files(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['MULTIPLE_UPLOAD'], filename))
                upload = True
        
        if (upload == True):
            # res = make_response(jsonify({"message": f"Los PDFs fueron cargado con éxito."}), 200)
            # return res
            # resultLoad = True
            print('File(s) successfully uploaded')
            # return redirect('/extract_mul')
            return render_template('extract_mul.html', resultLoad=upload)

@app.route("/action_extract_mul", methods=["GET", "POST"])
def action_extract_mul():
    result_process = False

    if request.method == "POST":
        global file_pdf, resultText, file_show #resultAlert
        (resultText, file_show) = ("", "")

        # Verify if posible to process
        if get_viewProcess_CPU() is True :
            path = os.path.join(app.config['SINGLE_UPLOAD'],file_pdf)
            fname = os.listdir(app.config['SINGLE_SPLIT']) #fname: List contain pdf documents names in folder
            # 1. SPLIT PDF
            # print("\n------------------- START SPLIT PROCESS -------------------")
            pdf_remove(fname)       # Call pdf remove function
            pdf_splitter(path)      # Call pdf splitter function
            # 2. Process PDF
            # print("\n------------------ START EXTRACT PROCESS ------------------")
            result_process = pdf_process()           # Call pdf process function
            print("Out web: " + app.config['SINGLE_FORWEB'])
            if result_process == True :
                # mask_imageOut = os.path.join(app.config['PATH_OUT_FORWEB'], (sub+file_image))
                file_show = file_pdf.split(".pdf")[0]
                # read the background from "background.txt" o "background.docx"
                resultText = app.config['SINGLE_FORWEB']+'/background.docx'
            # else:
            #     resultAlert = "No fue posible procesar la imagen"
        else:
            file_show = "None"
            # resultAlert = "El servidor está procesando, debe esperar un momento."
    
    print("Res: " + str(resultText))
    return render_template('extract_mul.html', resultText=resultText, file_show=file_show)

# INIT PROJECT
if __name__ == '__main__':
    # start the flask app
    app.run(debug=True, use_reloader=True)