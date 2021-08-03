# ExtractPDF

ExtractPDF is an script that get data page by page in order to consolidate the information in the next format:
- title pdf
- author name
- objective
- metholodogy (design, approach, level)
- samples
- tools
- conclusions
- background

## Installation
* The version based on python scripts use 'extract.py' to run split and process PDF
  python3 extract.py

* The web version does not use scripts, you just have to deploy the source code on the server and apply the appropriate configuration for the Flask Python Project
  1st, extract data from single (1) PDF document (OK)
  2nd, extract data from multiple (N) PDF documents (...)