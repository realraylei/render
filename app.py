from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pdf2docx import Converter
import tempfile, os

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({'ok': True})

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'ok': False, 'msg': '未收到文件'}), 400
    f = request.files['file']
    if not f.filename.lower().endswith('.pdf'):
        return jsonify({'ok': False, 'msg': '仅支持 PDF 文件'}), 400
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, 'input.pdf')
        out = os.path.join(d, 'output.docx')
        f.save(src)
        try:
            cv = Converter(src)
            cv.convert(out)
            cv.close()
            return send_file(out, as_attachment=True,
                             download_name='converted.docx',
                             mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        except Exception as e:
            return jsonify({'ok': False, 'msg': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
