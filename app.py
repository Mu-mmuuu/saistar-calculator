from flask import Flask, render_template, request, jsonify
# import mysql.connector
import pandas as pd
import subprocess
from calculator import score_calculator

app = Flask(__name__,static_folder = "./static/")

@app.route("/")
def index():
  return render_template("index.html")

@app.route('/execute-command',methods=['GET'])
def execute_command():
    command = request.args.get('command')
    if not command:
        return jsonify(error='No command provided.')
    try:
        # 入力されたコマンドを安全に実行する
        result = subprocess.check_output(command.split(), stderr=subprocess.STDOUT)
        result_str = result.decode('utf-8').strip() # バイト列を文字列に変換して改行を削除
        return jsonify(result=result_str) # レスポンスをJSON形式で返す
    except subprocess.CalledProcessError as e:
        # コマンドの実行に失敗した場合
        return jsonify(error=e.output.decode('utf-8').strip()) # エラーメッセージを返す

if __name__ == '__main__':
    app.run(debug=True)

