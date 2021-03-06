# coding: utf-8
import os
from flask import Flask, request, send_from_directory,jsonify
import time
from qiniu import Auth, put_file, etag
import qiniu.config

UPLOAD_FOLDER='guisheng_pics'
ALLOWED_EXTENSIONS=set(['png','jpg','jpeg','svg'])
ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
BUCKET_NAME = 'guisheng'

q = Auth(ACCESS_KEY, SECRET_KEY)

app = Flask(__name__)

@app.route('/guisheng/upload_pics/',methods = ['POST'])
def upload_pics():
    if request.method == 'POST':
        file = request.files['file']
        if file and ('.' in file.filename and file.filename.split('.',1)[1] in ALLOWED_EXTENSIONS):
            fname = '.'.join([str(int(time.time())),file.filename.split('.',1)[1]])
            file.save(os.path.join(UPLOAD_FOLDER,fname))
            localfile = ''.join([UPLOAD_FOLDER,'/',fname])
            key = '.'.join([str(int(time.time())),file.filename.split('.',1)[1]])
            token = q.upload_token(BUCKET_NAME, key, 3600)
            ret, info = put_file(token, key, localfile)
            pic_url = "".join(["http://ouno0zh2y.bkt.clouddn.com/",key])
            os.remove(os.path.join(UPLOAD_FOLDER,fname))
            return jsonify({
                'pic_url':pic_url
            })

@app.route('/guisheng/delete_pics/',methods = ['POST'])
def delete_pics():
    if request.method == 'POST':
        pic_url = request.get_json().get('pic_url')
        filename = pic_url.split('/')[-1]
        os.remove(os.path.join(UPLOAD_FOLDER,filename))
        return jsonify({'filename':filename}),200

@app.route('/guisheng_pics/<filename>/',methods = ['GET','POST'])
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=7777)

