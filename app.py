from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.fm6vi.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/toy", methods=["POST"])
def toy_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'title':title,
        'image':image,
        'desc':desc,
        'comment':comment_receive
    }
    db.toy.insert_one(doc)

    return jsonify({'msg': 'DB에 저장!'})


@app.route("/toy", methods=["GET"])
def toy_get():
    toy_list = list(db.toy.find({}, {'_id': False}))
    return jsonify({'toy': toy_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
