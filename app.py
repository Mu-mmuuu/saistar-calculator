from flask import Flask, render_template, request, jsonify
# import mysql.connector
import pandas as pd
import subprocess
from calculator import score_calculator

app = Flask(__name__,static_folder = "./static/")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # POSTリクエストからデータを取得
        data = request.get_json()
        song_name = data['song_name']
        idol_number = [int(x) for x in data['idol_number']]
        appeal = int(data['appeal'])
        Pskill_name = data['Pskill_name']
        Pskill_Lv = int(data['Pskill_Lv'])
        trial = int(data['trial'])

        # 計算結果を返す
        score = score_calculator(song_name, idol_number, appeal,Pskill_name,Pskill_Lv,trial)
        return jsonify(score)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

