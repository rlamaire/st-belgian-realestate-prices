import streamlit as st
import pandas as pd
import requests, zipfile, io

st.title('Vastgoed Prijzen Overzicht')

@st.cache_data
def read_data():

    r = requests.get('https://statbel.fgov.be/sites/default/files/files/opendata/immo/vastgoed_2010_9999.zip')
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("data")


    df = pd.read_table('data/vastgoed_2010_9999.txt',sep='|',encoding='latin-1')
    df.drop('CD_TYPE_FR',axis=1,inplace=True)
    df.drop('CD_REFNIS_FR',axis=1,inplace=True)
    df.drop('CD_REFNIS',axis=1, inplace=True)
    df.drop('CD_CLASS_SURFACE',axis=1,inplace=True)
    df.dropna(axis=0)


    df.columns=['year','type','location','period','total_transactions','25th percentile','median','75th percentile','geo_level']
    df = df[~df.period.str.contains('S')]
    df['year']=df['year'].astype(str)
    df['location'] = df['location'].str.title()


    gemeente_df_quarterly = df[(df.geo_level==5) & (df.period.str.contains('Q'))]
    gemeente_df_quarterly['date']= pd.to_datetime(gemeente_df_quarterly[['year','period']].apply('-'.join,axis=1))
    gemeente_df_quarterly.year = gemeente_df_quarterly.year.astype(int)

    gemeente_df_yearly = df[(df.geo_level==5) & (df.period.str.contains('Y'))]
    gemeente_df_yearly['date']= pd.to_datetime(gemeente_df_yearly.year)
    gemeente_df_yearly.year = gemeente_df_yearly.year.astype(int)

    return df , gemeente_df_quarterly , gemeente_df_yearly

df , gemeente_df_quarterly , gemeente_df_yearly = read_data()


category_list = ['Alle']
category_list.extend(gemeente_df_quarterly.type.unique())

col1 , col2 = st.columns(2)
category = col1.selectbox('Kies de category',category_list)
location = col2.selectbox('Kies de gemeente',gemeente_df_quarterly.location.unique())

graph_loc = st.empty()
st.subheader('Meest Recente mediaan prijzen')
if category == 'Alle':
    data = gemeente_df_quarterly[gemeente_df_quarterly.location == location]
    d = pd.pivot_table(data,values='median',index = 'date',columns='type')
    graph_loc.line_chart(data = d)
    cols = st.columns(len(d.columns))
    index = 0
    for i in d.columns:
        cols[index].metric(i,
                d[i].iloc[-1],
                delta=(d[i].iloc[-1] - d[i].iloc[-2]),
                help="""De prijs is de mediaan prijs. De aangeduide toename of afname is ten opzichte van het vorige jaar.""")
        index += 1
else: 
    data = gemeente_df_quarterly[(gemeente_df_quarterly.type==category)
                        & (gemeente_df_quarterly.location == location)]
    graph_loc.line_chart(data = data, x='date',y='median')
    st.metric(category,
            data['median'].iloc[-1],
            delta=(data['median'].iloc[-1] - data['median'].iloc[-2]),
            help="""De prijs is de mediaan prijs. De aangeduide toename of afname is ten opzichte van het vorige jaar.""")