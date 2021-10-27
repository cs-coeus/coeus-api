import os
from werkzeug.utils import secure_filename
import docx2txt
import requests

UPLOAD_DIRECTORY = "api_uploaded_files"
ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'docx', 'txt'])

class FileParser:

    @staticmethod
    def parse_file(file):
        if not os.path.exists(UPLOAD_DIRECTORY):
            os.makedirs(UPLOAD_DIRECTORY)
        if file and FileParser.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            stored_file = os.path.join(UPLOAD_DIRECTORY, filename)
            file.save(stored_file)
            extension = FileParser.file_extension(stored_file)
            if extension == 'txt':
                content = FileParser.parse_txt(stored_file)
            elif extension == 'docx':
                content = FileParser.parse_docx(stored_file)
            elif extension == 'doc':
                content = FileParser.parse_docx(stored_file)
            elif extension == 'pdf':
                content = FileParser.parse_pdf(stored_file)
            else:
                content = ''
            os.remove(stored_file)
            return content
        else:
            # wrong extension
            os.remove(os.path.join(UPLOAD_DIRECTORY, file))
            return ''

    def parse_pdf(file):
        payload = {}
        files = [
            ('file', ('pdf_file',
                      open(file, 'rb'),
                      'application/pdf'))
        ]
        headers = {
            'Content-type': 'application/pdf',
            'Accept': 'text/plain'
        }
        response = requests.request("PUT", "http://coeus.sit.kmutt.ac.th/api/apache/tika/tika", headers=headers, data=payload, files=files)
        return response.text

    def parse_docx(file):
        return docx2txt.process(file)

    def parse_txt(file):
        return open(file).read()

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def file_extension(filename):
        return filename.rsplit('.', 1)[1].lower()