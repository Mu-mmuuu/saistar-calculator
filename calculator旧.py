# %%time
def score_calculator():
    import math
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    import time
    from flask import Flask, render_template
    import mysql.connector

    cnx = None
    cnx = mysql.connector.connect(
    user='SideMuser',
    password='Altessimo@SEM315',
    host='localhost',
    database = 'sidem'
    )
    cursor = cnx.cursor()
    sql= "select * from idol"
    cursor.execute(sql)
    rows = cursor.fetchall()
    DB_idol = pd.DataFrame(rows, columns=[x[0] for x in cursor.description])
    inputdf = pd.DataFrame(columns = DB_idol.columns)

    cursor2 = cnx.cursor()
    sql2 = "select * from song"
    cursor2.execute(sql2)
    rows2 = cursor2.fetchall()
    database_song = pd.DataFrame(rows2, columns=[x[0] for x in cursor2.description])

    cursor3 = cnx.cursor()
    sql3 = "select * from time"
    cursor3.execute(sql3)
    rows3 = cursor3.fetchall()
    database_time = pd.DataFrame(rows3, columns=[x[0] for x in cursor3.description])

    cursor4 = cnx.cursor()
    sql4 = "select * from type"
    cursor4.execute(sql4)
    rows4 = cursor4.fetchall()
    database_type = pd.DataFrame(rows4, columns=[x[0] for x in cursor4.description])

    cursor5 = cnx.cursor()
    sql5 = "select * from notes_rate"
    cursor5.execute(sql5)
    rows5 = cursor5.fetchall()
    database_notes_rate = pd.DataFrame(rows5, columns=[x[0] for x in cursor5.description])

    cursor5 = cnx.cursor()
    sql5 = "select * from notes_rate"
    cursor5.execute(sql5)
    rows5 = cursor5.fetchall()
    database_notes_rate = pd.DataFrame(rows5, columns=[x[0] for x in cursor5.description])

    cursor6 = cnx.cursor()
    sql6 = "select * from Pskill"
    cursor6.execute(sql6)
    rows6 = cursor6.fetchall()
    Pskill_df = pd.DataFrame(rows6, columns=[x[0] for x in cursor6.description])

    cnx.close()



    song_name ='MES'
    appeal = '158900'
    idol = [120,163,337,388,403,454]

    for i in idol:
        i = int(i)
        inputdf = pd.concat([inputdf,DB_idol[DB_idol.index==i-1]])
    inputdf = inputdf.iloc[:,:12]

    Pskill_name_original = '延長'

    if Pskill_name_original in ['延長','確率UP','効果UP']:
        Pskill_Lv = '3'
        Pskill_Lv = int(Pskill_Lv)
        Pskill_Lv_original = Pskill_Lv
    else:
        Pskill_Lv = 1
        Pskill_Lv_original = ""

        
    #入力情報の整理
        
    song_name =database_song.index[database_song['name']==song_name]+1
    song_name = song_name.tolist()[0]
    lv = int(database_song.loc[song_name-1,'lv'])

    appeal = int(appeal)
    skill_name_original = inputdf['skill_name'].tolist()
    interval = inputdf['skill_interval'].tolist()
    skill_percent = inputdf['skill_percent'].tolist()
    skill_rate = inputdf['skill_value'].tolist()

    for i,n in enumerate(skill_name_original):
        if n == 'スコアアップ' or n == 'オーバーロード' or n == 'フォーカス':
            skill_name_original[i] ='score'
        elif n == 'コンボボーナス' or n == 'オーバーヒート':
            skill_name_original[i] = 'combo'
        elif n =='ダブルブースト':
            skill_name_original[i] = 'dobble'
        else:
            skill_name_original[i] = 'else'



    skill_percent = [int(p)/100 for p in skill_percent]
    skill_rate = [1+int(r)/100 for r in skill_rate]

    if Pskill_name_original == '延長':
        Pskill_name = 'expand'
    elif Pskill_name_original == '確率UP':
        Pskill_name = 'chance'
    elif Pskill_name_original == '効果UP':
        Pskill_name = 'enhance'
    else:
        Pskill_name = 'support'
        
    if Pskill_Lv == 1:
        Pskill_Lv_original = ""
    else:
        Pskill_Lv_original = Pskill_Lv

        
        
    #各種変数の定義

    #試行回数(変更可能。1000で10秒、10000で計算時間2分ほど)
    trial = 1000

    #楽曲関連
    song_lv_ef = round(0.1052 * lv + 2.6144 , 2)
    accuracy = 1
    mode = 'normal'

    np_floor = np.floor
    math_floor = math.floor
    np_sum = np.sum



    #スキル発動を判定する関数を定義
    def random_skill(song,song_withskill,skill_rate,skill_percent,skill_name,skill_acts):
        song_copy = song.copy()
        song_loc = song_copy.loc
        song_columns = song_copy.columns
        random_choices = random.choices
        random_result_dict = {} 
        for acts, s,r,p,li in zip(skill_acts,skill_name,skill_rate,skill_percent,song_withskill):
            if s == 'support' :
                continue
            random_result = random_choices([1.0, r], weights = [1-p,p], k=len(acts))
            
            if Pskill_name == 'enhance':
                for  t in Pskill_timing:
                    j = df_skilltiming.index[(df_skilltiming[s] - t >=0) & (df_skilltiming[s] - t < Pskill_time)].tolist()
                    if j == []:
                        continue
                    random_result[j[0]-1] = random_choices([1.0,r*Pskill_value],weights = [1-p,p],k=1)[0]
            
            if Pskill_name == 'chance':
                for  t in Pskill_timing:
                    j = df_skilltiming.index[(df_skilltiming[s] - t >=0) & (df_skilltiming[s] - t < Pskill_time)].tolist()
                    if j == []:
                        continue
                    random_result[j[0]-1] = random_choices([1.0,r],weights = [1-(p*Pskill_value),p*Pskill_value],k=1)[0]
                        
            random_result_df = pd.DataFrame({s:random_result})
            random_result_df.index += 11
            random_result_dict.update(random_result_df.to_dict())
            
        song_copy = song_copy.replace(random_result_dict)    
        score_columns = [c for c in song_columns if 'score' in c]
        combo_columns = [c for c in song_columns if 'combo' in c]
        dftempscore = song_copy[score_columns]
        dftempcombo = song_copy[combo_columns]
        
        if 'dobble' in skill_name:
            dobbleboost_columns = [c for c in song_columns if 'dobble' in c]
            dftempdobble = song_copy[dobbleboost_columns]
            dftempdobble['skill'] = np.max(dftempdobble,axis = 1)-1
            if 'score' in skill_name_original:
                song_copy['S_skill'] = np.max(dftempscore,axis = 1) + dftempdobble['skill']
            if 'combo' in skill_name_original:
                song_copy['C_skill'] = np.max(dftempcombo,axis = 1) + dftempdobble['skill']
        else:
            if 'score' in skill_name_original:
                song_copy['S_skill'] = np.max(dftempscore,axis = 1)
            if 'combo' in skill_name_original:
                song_copy['C_skill'] = np.max(dftempcombo,axis = 1)
        return song_copy



    # ノーツごとの得点を計算する関数を定義
    def each_score(song):
        base = math_floor(appeal * song_lv_ef / notes[-1])
        combo_rate = np.array(song['conbo_rate'])
        notes_rate = np.array(song['notes_rate'])
        S_skill = np.array(song['S_skill'])
        C_skill = np.array(song['C_skill'])
        temp0 = np_floor(base*accuracy)
        temp1 = np_floor(temp0*combo_rate)
        temp2 = np_floor(temp1*notes_rate)
        temp3 = np_floor(temp2*S_skill)
        score_list = np_floor(temp3*C_skill)
        total_score = np_sum(score_list)
        total_after_special = np_sum(score_list[:SP_notes+1])
        return total_score, total_after_special

    #スキルを加味したスコアを計算する関数を定義
    def each_score_withskill(song,song_withskill,skill_rate,skill_percent,skill_name,skill_acts):
        song_random = random_skill(song,song_withskill,skill_rate,skill_percent,skill_name,skill_acts)
        return each_score(song_random)



    #必要データを読み込み


    # database = pd.read_excel(filename,sheet_name=['time','type','notes_rate'])
    database_time = database_time[str(song_name)]
    database_type = database_type[str(song_name)]
    database_notes_rate = database_notes_rate[str(song_name)]



    song = pd.concat([database_time,database_type,database_notes_rate],axis=1)
    song = song.dropna(how='any')
    song.index += 1
    song.columns = ['time','type','notes_rate']
    song['conbo_rate'] = None

    # Pskill_df = pd.read_excel(filename,sheet_name='Pskill')
    Pskill_df = Pskill_df[(Pskill_df['name'] == Pskill_name) & (Pskill_df['Lv'] == Pskill_Lv)]
    Pskill_time = float(Pskill_df['time'])
    Pskill_value = float(Pskill_df['effect size'])

    Pskill_timing =list(song.loc[song['type'] == 'pskill','time'])

    SP_notes = song.index[song['type'] == 'special'][0]
    SP_notes = int(SP_notes)
    P_notes = list(song.index[song['type'] == 'pskill'])

    skill_name = [1,2,3,4,5,6]
    for i,s in enumerate(skill_name_original):
        skill_name[i] = s + str(i+1)
        song[skill_name[i]] = 1.0
    song['S_skill'] = 1.0
    song['C_skill'] = 1.0

    notes = list(song.index)
    last_note = notes[-1]

    #楽曲ごとのコンボ倍率を算出
    comboplus_timing = np.array([0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9])
    comboplus_timing = np.floor(comboplus_timing * last_note) +1
    if mode == 'normal':
        comboplus_num = [1.0,1.01,1.02,1.03,1.05,1.08,1.1,1.15,1.2,1.3,1.4]
    else:
        comboplus_num = [1.0,1.01,1.03,1.05,1.08,1.12,1.17,1.25,1.35,1.5,1.7]
    comboplus_timing = list(comboplus_timing)

    #コンボ倍率のリスト作成
    for i,ct in enumerate(list(comboplus_timing)):
        song['conbo_rate'].loc[song.index >= ct] = comboplus_num[i]
        
        

    # スキルがかかるノーツリストを作成
    song_loc = song.loc
    for s,i,r in zip(skill_name,interval,skill_rate):
        song.loc[(song['time'] // i >=1) & (song['time'] % i < math.ceil(i/2)),s] = song['time'].loc[(song['time'] // i >=1) & (song['time'] % i < math.ceil(i/2))] // i + 10
    song_withskill = [list(song.index[song[s] >= 10]) for s,r in zip(skill_name,skill_rate) ]
    skill_maxact = [np.max(song[s]) -10 for s in skill_name]
    skill_acts = [range(1,int(sm+1)) for sm in skill_maxact]

    #プロデューサースキルと照合するための表作成     
    df_skilltiming = pd.DataFrame()
    for i,s in enumerate(skill_name):
        for ac in skill_acts[i]:
            start = song['time'][song[s] == (ac+10)]
            df_skilltiming.loc[ac,s] = np.min(start)

    #スキル延長処理               
    if Pskill_name == 'expand':
        for s,i in zip(skill_name,interval):
            for  t in Pskill_timing:
                for n in df_skilltiming.index:
                    if np.isnan(df_skilltiming.loc[n,s]):
                        continue
                    if df_skilltiming.loc[n,s] - t < Pskill_time:
                        song.loc[(song['time'] >= n*i) & (song['time'] % i < math.ceil(i/2)* Pskill_value),s] = n+10

                        


    #試行回数の分だけ実際に計算
    theory_percent = [1,1,1,1,1,1]
    min_percent = [0,0,0,0,0,0]

    results = [each_score_withskill(song,song_withskill,skill_rate,skill_percent,skill_name,skill_acts) for i in range(trial)]
    theory_score = each_score_withskill(song,song_withskill,skill_rate,theory_percent,skill_name,skill_acts)
    min_score = each_score_withskill(song,song_withskill,skill_rate,min_percent,skill_name,skill_acts)
    results.append(theory_score)
    results.append(min_score)

    results_df = pd.DataFrame(data=results,columns= ['スコア','SPノーツ直後'])
    total_df = pd.DataFrame(data= results_df['スコア'] )
    SP_df = pd.DataFrame(data= results_df['SPノーツ直後'] )


    # 結果出力
    fullname = database_song.loc[song_name-1,'full_name']
    # print('アピール値: ' + str(appeal))
    # print('Pスキル： '+ Pskill_name_original,Pskill_Lv_original)

    percentile_list = [1,.999,.995,.99, .97, .95, .9, .5,0]
    percentile_index = ['max','0.1%','0.5%','1%','3%','5%','10%','50%','min']
    dflast = total_df.quantile(q=percentile_list)
    dflast.index = percentile_index
    # dflast['確率']=  ['max','0.1%','0.5%','1%','3%','5%','10%','50%','min']

    SP_df = SP_df.quantile(q=percentile_list)
    SP_df.index = percentile_index
    dflast = pd.concat([dflast,SP_df],axis=1)
    dflast = dflast.astype(int)

    # pd.options.display.float_format = '{:.0f}'.format
    # display(dflast)
    return dflast, fullname, appeal,Pskill_name_original,Pskill_Lv_original,inputdf