import streamlit as st
from datetime import time
import pandas as pd

def time_estimate(loc1,loc2):
    x1,y1=travel_df[travel_df['景點地名']==loc1].loc[:,'經度'].iloc[0],travel_df[travel_df['景點地名']==loc1].loc[:,'緯度'].iloc[0]
    x2,y2=travel_df[travel_df['景點地名']==loc2].loc[:,'經度'].iloc[0],travel_df[travel_df['景點地名']==loc2].loc[:,'緯度'].iloc[0]

    print(x1,y1)
    print(x2,y2)
    print(((x1-x2)**2+(y1-y2)**2)**0.5)
    d=((x1-x2)**2+(y1-y2)**2)**0.5
    if d<0.025:
        return 10
    else:
        return 10+int(d//0.05+1)*10

def loc_time(loc):
    return travel_df[travel_df['景點地名']==loc].loc[:,'時間'].iloc[0]



st.title('AI search 高雄觀光景點')

#st.subheader('室內/室外')
io = st.selectbox('室內/室外',('室內','室外'))

#st.subheader('行政區')
area = st.multiselect("行政區",['不限','鹽埕區','鼓山區','左營區','楠梓區','三民區','新興區','前金區','苓雅區','前鎮區','旗津區','小港區','鳳山區','林園區','大寮區','大樹區','大社區','仁武區','鳥松區','岡山區','橋頭區','燕巢區','田寮區','阿蓮區','路竹區','湖內區','茄萣區','永安區','彌陀區','梓官區','旗山區','美濃區','六龜區','甲仙區','杉林區','內門區','茂林區','桃源區','那瑪夏區'],placeholder='不限')

#st.subheader('預算花費')
cost = st.slider('預算花費', min_value=0, max_value=1000, value=100, step=100)

#st.subheader('靜態/動態')
move = st.radio("靜態/動態",['靜態','動態'],index=None,)

#st.subheader('時間')
time_ = st.slider("時間",value=(time(11, 30), time(12, 45)))
time_display=f'{time_[0].hour}:{time_[0].minute} ~ {time_[1].hour}:{time_[1].minute}'
st.write(time_display)


#st.subheader('性質')
kind = st.multiselect("性質",['宗教巡禮','建築之美','悠閒泡湯','藍色水岸','觀光工廠','浪漫婚紗','軍旅探索','戶外踏青','夜市商圈','歷史文化','風景區','藝文館所','親子同遊','人權景點'],placeholder='-')

keyword = st.text_input("關鍵字", "")

def result():
    query=f'從資料內找出最佳的景點(只輸出景點名稱即可)，需是{io}、位於{area}附近、花費小於{cost}且是{move}的，性質包含{kind}，時段為{time_display}，關鍵字為{keyword}。'
    st.write(query)

if st.button(label="Submit",type="primary"): result()


#-------------------------------------------------------------------------------------------------------------------------------------------------------------


loc_list=["光榮碼頭","蓮池潭風景區","玫瑰聖母聖殿主教座堂","高雄燈塔(旗津旗后燈塔)","新光碼頭","茂林谷","高雄市文化中心"]

travel_df=pd.read_csv('D:\code\streamlit\data.csv')

st.markdown(travel_df[travel_df['景點地名']=='愛河'].loc[:,'類型'].iloc[0])


df = pd.DataFrame(
    data = [{'Select': False, "Location": i, "Sort": travel_df[travel_df['景點地名']==i].loc[:,'類型'].iloc[0], "Time(min)": loc_time(i)} for i in loc_list]
)


edited_df = st.data_editor(df,use_container_width=True,hide_index=True)

selection = edited_df.loc[edited_df["Select"] == True]["Location"].tolist()

st.markdown(selection)

if st.button('submit'):
    if len(selection)>3:
        st.warning('請勿選擇大於3個景點', icon="⚠️")
    elif len(selection)<3:
        st.warning(f'請選擇3個景點，尚缺{3-len(selection)}個景點', icon="⚠️")
    else:
        trans_time,trans_url=[],[]
        for i in range(2):
            trans_time.append(time_estimate(selection[i],selection[i+1]))
            trans_url.append('https://www.google.com/maps/dir/'+selection[i]+'/'+selection[i+1])

        container = st.container(border=True)
        container.markdown(f"""
            ## 行程表:
            <div style='
                background-color: #f0f0f0;
                border: 2px solid #000000;
                border-radius: 6px;
                padding: 8px;
                box-shadow: 1px 1px 5px #888888;
            '>
                <h3 style='color: #000000;'>{selection[0]}</h3>
                <p style='color: #000000;'>{loc_time(selection[0])}分鐘 | 0:00~0:00</p>
            </div>

            **<font size=4>:oncoming_automobile: 約{trans_time[0]}分鐘</font>**   [:mag_right: Google Map]({trans_url[0]})

            <div style='
                background-color: #f0f0f0;
                border: 2px solid #000000;
                border-radius: 6px;
                padding: 8px;
                box-shadow: 1px 1px 5px #888888;
            '>
                <h3 style='color: #000000;'>{selection[1]}</h3>
                <p style='color: #000000;'>{loc_time(selection[1])}分鐘 | 0:00~0:00</p>
            </div>

            **<font size=4>:oncoming_automobile: 約{trans_time[1]}分鐘</font>**   [:mag_right: Google Map]({trans_url[1]})
            <div style='
                background-color: #f0f0f0;
                border: 2px solid #000000;
                border-radius: 6px;
                padding: 8px;
                box-shadow: 1px 1px 5px #888888;
            '>
                <h3 style='color: #000000;'>{selection[2]}</h3>
                <p style='color: #000000;'>{loc_time(selection[2])}分鐘 | 0:00~0:00</p>
            </div>

                    """,unsafe_allow_html=True)