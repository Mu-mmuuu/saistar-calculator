from flask import Flask, render_template
import mysql.connector
import pandas as pd
from calculator import score_calculator

app = Flask(__name__,static_folder = "./static/")

cnx = None
cnx = mysql.connector.connect(
  user='SideMuser',
  password='Altessimo@SEM315',
  host='localhost',
  database = 'sidem'
  )
cursor = cnx.cursor()
sql= "select No, path, rarity, idol_type, photo_name, idol_name, center_skill, skill_name, mixskill_name, skill_interval, skill_percent, skill_value from idol"
cursor.execute(sql)
rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=[x[0] for x in cursor.description])
idolheader = ['No.','画像','レアリティ','属性','フォト名','アイドル名','センター効果','スキル名','混合スキル名','秒数(s)','確率(%)','効果量(%)']
idoldata = df.values.tolist()


cursor2 = cnx.cursor()
sql2= "select * from song"
cursor2.execute(sql2)
rows2 = cursor2.fetchall()

df2 = pd.DataFrame(rows2, columns=[x[0] for x in cursor2.description])
songheader = ['No.','画像','曲名','属性','楽曲Lv','略称']
songdata = df2.values.tolist()

cnx.close()


# @app.route("/")

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/form")
def form():
  return render_template("form.html")


@app.route("/idollist")
def idollist():
  return render_template("idollist.html",idolheader=idolheader, idoldata = idoldata)

@app.route("/songlist")
def songlist():
  return render_template("songlist.html",songheader=songheader, songdata = songdata)

@app.route("/result")
def show_result():
  result = score_calculator()
  dflast = result[0]
  song_fullname = result[1]
  appeal = result[2]
  Pskill_fullname = result[3]
  Pskill_Lv_original = result[4]
  inputdf= result[5]
  # resultidolheader = idolheader
  resultidolheader = inputdf['No'].tolist()
  # resultidoldata = inputdf.values.tolist()
  resultidoldata = inputdf['path'].values.tolist()
  # resultheader = ['スコア']
  resultheader = dflast.columns
  resultdata = dflast.values.tolist()
  percentile_index = ['max','0.1%','0.5%','1%','3%','5%','10%','50%','min']
  return render_template("result.html",
    resultheader=resultheader, resultdata = resultdata,
    song_fullname=song_fullname,appeal=appeal,
    Pskill_fullname=Pskill_fullname,
    Pskill_Lv_original=Pskill_Lv_original,
    resultidolheader=resultidolheader,resultidoldata=resultidoldata,
    percentile_index=percentile_index)


if __name__ == '__main__':
  app.run()
