# coding: utf-8
import os
from flask import Flask, request, send_from_directory,jsonify
import time

UPLOAD_FOLDER='guisheng_pics'
ALLOWED_EXTENSIONS=set(['png','jpg','jpeg','svg'])

app = Flask(__name__)
@app.route('/guisheng/upload_pics/',methods = ['POST'])
def upload_pics():
    if request.method == 'POST':
        file = request.files['file']
        if file:#and ('.' in filename and filename.split('.',1)[1] in ALLOWED_EXTENSIONS):
            fname = '.'.join([str(int(time.time())),file.filename.split('.',1)[1]])
            file.save(os.path.join(UPLOAD_FOLDER,fname))
            pic_url = os.path.join('http://120.24.4.254:7777/',UPLOAD_FOLDER,fname)
        return jsonify({
            'pic_url':pic_url
        })

@app.route('/guisheng/delete_pics/',methods = ['POST'])
def delete_pics():
    if request.method == 'POST':
        img_url = request.get_json().get('img_url')
        filename = img_url.split('/')[-1]
        os.remove(os.path.join(UPLOAD_FOLDER,filename))
        return jsonify({'filename':filename}),200

@app.route('/guisheng_pics/<filename>/',methods = ['GET','POST'])
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5431)

