import math
import pandas as pd
import numpy as np
import random

def score_calculator(song_name,idol_number,appeal,Pskill_name,Pskill_Lv,trial):    
# def calculator(song_name,appeal,idol,Pskill_fullname,Pskill_Lv,trial):

    filename = './static/B_スコア予測用data_2.4.xlsx'
    DB_song = pd.read_excel(filename,index_col='No',sheet_name='song')
    DB_song.reset_index(inplace=True)
    DB_song = DB_song.to_numpy()

    DB_idol_df = pd.read_excel(filename,index_col=0,sheet_name='idol')
    DB_idol_df.reset_index(inplace=True)
    DB_idol = DB_idol_df.to_numpy()

    #入力値処理
    if trial == 0:
        trial = 1000
    elif trial > 10000:
        trial = 10000
    else:
        trial = trial

    song_data = DB_song[np.any(DB_song==song_name,axis=1)][0]
    song_No = song_data[0]
    song_No = int(song_No)
    song_fullname = song_data[1]
    song_lv = song_data[4]

    appeal = int(appeal)

    song_lv_ef = round(0.1052 * song_lv + 2.6144 , 2)
    accuracy = 1
    mode = 'normal'
    idol = np.array(idol_number,dtype=int)
    idol -= 1
    idol_data = DB_idol[[idol[0],idol[1],idol[2],idol[3],idol[4],idol[5]],:]

    inputdf = pd.DataFrame(idol_data,columns= DB_idol_df.columns,index=idol_data[:,0])
    inputdf = inputdf.drop(['No','センター効果','スキル_後半','vo','da','vi','計','日付'],axis=1)
    inputdf.rename(columns ={'スキル_前半':'スキル'}, inplace =True)

    skill_fullname = idol_data[:,6]
    interval = idol_data[:,8]
    skill_percent = idol_data[:,9]/100
    skill_rate = 1+idol_data[:,10]/100

    skill_name = skill_fullname.copy()
    np.place(skill_name,skill_name == 'スコアアップ','score')
    np.place(skill_name,skill_name == 'オーバーロード','score')
    np.place(skill_name,skill_name == 'フォーカス','score')
    np.place(skill_name,skill_name == 'コンボボーナス','combo')
    np.place(skill_name,skill_name == 'オーバーヒート','combo')
    np.place(skill_name,skill_name == 'ダブルブースト','boost')
    np.place(skill_name,skill_name == 'ダブルエフェクト','effect')
    np.place(skill_name,skill_name == '判定強化','else')
    np.place(skill_name,skill_name == 'ライフ回復','else')
    np.place(skill_name,skill_name == 'ダメージガード','else')

    if Pskill_name == 'expand':
        Pskill_fullname = '延長'
    elif Pskill_name == 'chance':
        Pskill_fullname = '確率UP'
    elif Pskill_name == 'enhance':
        Pskill_fullname = '効果UP'
    else:
        Pskill_fullname = 'その他'

    Pskill_Lv = int(Pskill_Lv)

    if Pskill_Lv == 1:
        Pskill_Lv_original = ""
    else:
        Pskill_Lv_original = Pskill_Lv


    #ノーツ配列を作成
    score_data = pd.read_excel(filename,sheet_name=['time','type','notes_rate'])
    notes = score_data['time'].to_numpy()[:,song_No]
    notes = len(notes[~np.isnan(notes)])

    score_data = np.vstack([score_data['time'].to_numpy()[:notes,song_No],
                           score_data['type'].to_numpy()[:notes,song_No],
                           score_data['notes_rate'].to_numpy()[:notes,song_No]
                          ])
    
    DB_Pskill = pd.read_excel(filename,sheet_name='Pskill')
    DB_Pskill = DB_Pskill.to_numpy()
    Pskill_data = DB_Pskill[np.any(DB_Pskill==Pskill_name,axis=1)][Pskill_Lv-1,:]
    Pskill_time = Pskill_data[2]
    Pskill_value = Pskill_data[3]

    Pskill_timing = np.where(score_data[1]=='pskill')
    Pskill_timing = np.squeeze(score_data[:,Pskill_timing])[0]

    SP_notes = int(np.where(score_data[1]=='special')[0])

    #楽曲ごとのコンボ倍率を算出
    comboplus_timing = np.array([0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9])
    comboplus_timing = np.floor(comboplus_timing * notes).astype(int) #+1

    if mode == 'normal':
        comboplus_num = np.array([1.0,1.01,1.02,1.03,1.05,1.08,1.1,1.15,1.2,1.3,1.4])
    else:
        comboplus_num = np.array([1.0,1.01,1.03,1.05,1.08,1.12,1.17,1.25,1.35,1.5,1.7])

    #コンボ倍率のリスト作成
    combo_rate = np.zeros(notes)
    for i in range(1,11):
        combo_rate[comboplus_timing[i-1]:comboplus_timing[i]] += comboplus_num[i-1]
    #     print(i)
    combo_rate[comboplus_timing[-1]:] += comboplus_num[-1]


    #スキル用の配列を作成
    skill_data = np.zeros((6,notes),dtype = int)

    for i in range(6):
        if skill_name[i] == 'effect': 
            interval_judge = np.where(score_data[0] % interval[i] < interval[i]*0.9) 
        else:
            interval_judge = np.where(score_data[0] % interval[i] < math.ceil(interval[i]/2)) 
        skill_data[i,interval_judge] += 10 + (score_data[0,interval_judge]//interval[i]).astype(int)

    np.place(skill_data,skill_data == 10, 0)
    np.place(skill_data,skill_data == 0, 1)

    skill_maxact = np.max(skill_data,axis=1)-10

    skilltiming = np.zeros((6,np.max(skill_maxact)))


    for i in range(6):
        for j in range(1,skill_maxact[i]+1):
            if j+10 not in skill_data[i]:
                continue
            skilltiming[i][j-1] = np.min(score_data[0][np.where(skill_data[i] == j+10)])

    #スキル延長処理               
    if Pskill_name == 'expand':
        for i in range(6):
            for  t in Pskill_timing:
                for n in range(np.max(skill_maxact)):
                    if skilltiming[i][n] == 0:
                        continue
                    if skilltiming[i][n] - t < Pskill_time and skilltiming[i][n] - t >= 0:
                        interval_judge = np.where((score_data[0] >= (n+1)*int(interval[i])) & (score_data[0] < (n+2)*int(interval[i])) &(score_data[0] % int(interval[i]) < math.ceil(int(interval[i])/2)* float(Pskill_value)))
                        skill_data[i,interval_judge] = 10 + (score_data[0,interval_judge]//int(interval[i])).astype(int)

    np.place(skill_data,skill_data == 10, 0)
    np.place(skill_data,skill_data == 0, 1)


    #スキル発動を判定する関数を定義

    random_result = np.zeros((6,np.max(skill_maxact)))

    def calculator(skill_percent):
        skill_calc = np.ones((6,notes))
        for i in range(6):
            if skill_name[i] == 'support':
                continue
            random_result[i] = random.choices([1.0, skill_rate[i]], weights = [1-skill_percent[i],skill_percent[i]], k=np.max(skill_maxact))
            if skill_maxact[i] < np.max(skill_maxact):
                random_result[i][skill_maxact[i]:] = 0

            if Pskill_name == 'chance':
                for  t in Pskill_timing:
                    for n in range(np.max(skill_maxact)):
                        if skilltiming[i][n] == 0:
                            continue
                        if skilltiming[i][n] - t < Pskill_time and skilltiming[i][n] - t >= 0:
                            random_result[i][n] = random.choices([1.0,skill_rate[i]],weights = [1-(skill_percent[i]*Pskill_value),skill_percent[i]*Pskill_value],k=1)[0]                             

            for j in range(np.max(skill_maxact)):
                if (interval[i]*(j+1) > score_data[0,SP_notes])&(interval[i]*(j+1) < score_data[0,SP_notes+1]):
                    skill_calc[i][np.where(skill_data[i] == j+11)] = 1
                else:
                    skill_calc[i][np.where(skill_data[i] == j+11)] = random_result[i][j]

        if Pskill_name == 'enhance':
            for t in Pskill_timing:
                Pskill_on = ((score_data[0] >= t) & (score_data[0] <= (t + Pskill_time)))
                for i in range(6):
                    skill_calc[i][np.where(Pskill_on)] = (skill_calc[i][np.where(Pskill_on)] - 1) * Pskill_value + 1        

        score_skillrate = skill_calc[np.where(skill_name == 'score')]
        combo_skillrate = skill_calc[np.where(skill_name == 'combo')]
        boost_skillrate = skill_calc[np.where(skill_name == 'boost')]
        boost_skillrate -= 1
        effect_skillrate = skill_calc[np.where(skill_name == 'effect')]
        effect_skillrate -= 1

        if len(score_skillrate) == 0:
            score_skillrate = np.ones((1,notes))

        if len(combo_skillrate) == 0:
            combo_skillrate = np.ones((1,notes))

        if len(boost_skillrate) == 0:
            boost_skillrate = np.zeros((1,notes))

        if len(effect_skillrate) == 0:
            effect_skillrate = np.zeros((1,notes))

        score_skillrate = np.max(score_skillrate,axis=0)
        combo_skillrate = np.max(combo_skillrate,axis=0)
        boost_skillrate = np.max(boost_skillrate,axis=0)
        effect_skillrate = np.max(effect_skillrate,axis=0)

        boost_skillrate[np.where(boost_skillrate > 0 )] += effect_skillrate[np.where(boost_skillrate > 0 )]

        score_skillrate += boost_skillrate
        score_skillrate[np.where(score_skillrate > 1 )] += effect_skillrate[np.where(score_skillrate > 1 )]
        combo_skillrate += boost_skillrate
        combo_skillrate[np.where(combo_skillrate > 1 )] += effect_skillrate[np.where(combo_skillrate > 1 )]


        base = math.floor(appeal * song_lv_ef / notes)
        base = np.floor(base*accuracy)
        notes_calc = np.vstack([score_data[-1],
                                combo_rate,
                                score_skillrate,
                                combo_skillrate])

        temp = np.zeros(notes)
        temp += base
        temp = np.floor(temp*notes_calc[0]) #notes_rate
        temp = np.floor(temp*notes_calc[1]) #combo_rate
        temp = np.floor(temp*notes_calc[2]) #score_skillrate
        notes_scores = np.floor(temp*notes_calc[3]) #combo_skillrate
        total_score = np.sum(notes_scores)
        total_afterSP = np.sum(notes_scores[:SP_notes+1])

        return np.array([total_score,total_afterSP])


    results = np.zeros((trial+2,2),dtype=int)
    for i in range(trial):
        results[i] = calculator(skill_percent)
    results[-1] = calculator(np.array([1,1,1,1,1,1]))
    results[-2] = calculator(np.array([0,0,0,0,0,0]))

    resultdf = pd.DataFrame(data=results,columns=['スコア','SPノーツ直後'])
    total_df = pd.DataFrame(data=results[:,0],columns=['スコア'])
    SP_df = pd.DataFrame(data=results[:,1],columns=['SPノーツ直後'])

    percentile_list = [1,.999,.995,.99, .97, .95, .9, .5,0]
    percentile_index = ['max','0.1%','0.5%','1%','3%','5%','10%','50%','min']
    dflast = total_df.quantile(q=percentile_list)
    dflast['スコア'] =dflast['スコア'].astype('int')
    dflast.index = percentile_index

    SP_df = SP_df.quantile(q=percentile_list)
    SP_df['SPノーツ直後'] =SP_df['SPノーツ直後'].astype('int')
    SP_df.index = percentile_index
    dflast = pd.concat([dflast,SP_df],axis=1)
    dflast.reset_index(inplace=True)
    dflast = dflast.rename(columns={'index':'　　　','スコア': 'スコア','SPノーツ直後': 'SPノーツ直後'})

    pd.options.display.float_format = '{:.0f}'.format
    
    dflast = dflast.to_html(index=False,table_id='result-table')
    inputdf = inputdf.to_html(table_id='input-table')

    return  song_fullname, appeal, Pskill_fullname, Pskill_Lv_original,inputdf, dflast, 