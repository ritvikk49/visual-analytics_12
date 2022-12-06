import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import altair as alt


#from vega_datasets import data
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import pyspark.sql.types as t
import pyspark.sql.functions as f

import pylab
import matplotlib 
from matplotlib import pyplot as plt
matplotlib.use('Agg') 


df = pd.read_csv("../transformed_dataset.csv")

st.set_page_config(
    page_title="Spotify Data Charts",
    page_icon="🎶",
    layout="centered"
)
st.markdown("""
<style>
.big-font {
    font-size:40px !important;
}
</style>
""", unsafe_allow_html=True)


st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSoQHBQOQbYXQV-ndDltVUSzv-VPOJdAX0mtg&usqp=CAU',use_column_width=True)

user_menu= st.sidebar.radio(
    'click on a Dashboard to view',
     ('Show the Columns to be displayed', 'Show Artists WordCloud of Popularity', 'Show Region Popularity','Show How many streams have the top 10 artists received overall','Show the Number of Streams by Region', 'Show number of days a song holds place in Top200', 'Show Correlation of Rank with Streams')
)

if user_menu=='Show the Columns to be displayed':
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect("Select",all_columns)
    new_df = df[selected_columns]
    st.dataframe(new_df)
    
    
if user_menu=='Show Artists WordCloud of Popularity':
    st.markdown('<p class="big-font"> Artist Popularity </p>', unsafe_allow_html=True)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    wc = WordCloud(max_font_size=130, min_font_size=25, colormap='tab20', background_color='grey', 
                           prefer_horizontal=.95, width=2100, height=700, random_state=0)
    counts = df['artist'].value_counts()
    cloud = wc.generate_from_frequencies(counts)
    plt.figure(figsize=(18,15))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    st.pyplot()


    
    
    
if user_menu=='Show Region Popularity':
    st.markdown('<p class="big-font"> Region Popularity </p>', unsafe_allow_html=True)
    wc = WordCloud(max_font_size=130, min_font_size=25, colormap='tab20', background_color='white', 
                           prefer_horizontal=.95, width=2100, height=700, random_state=0)
    counts = df['region'].value_counts()
    cloud = wc.generate_from_frequencies(counts)
    plt.figure(figsize=(18,15))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    st.pyplot()
    

    
if user_menu=='Show How many streams have the top 10 artists received overall':
    df.sort_values(by=['streams'])
    df10 = df.head(10)
    plt.figure(figsize=(8,8))
    sns.barplot(x=df10['artist'],
                y=df10['streams'], 
                palette="Paired")
    plt.xlabel("artist", size = 12)
    plt.ylabel("streams", size = 12)
    plt.title(" Number of Streams by Top 10 artists ", size = 18)
    plt.xticks(rotation = 90)
    plt.tight_layout()
    plt.show()
    st.pyplot()
    
    
if user_menu=='Show the Number of Streams by Region':
    #Pie Chart Visualization
    st.markdown('<p class="big-font"> Streams by Region </p>', unsafe_allow_html=True)
    #st.text("Streams by Region")
    streams = df.groupby('region')['streams'].sum().reset_index()

    # compute percent stream
    streams['percent_streams'] = streams['streams']/streams['streams'].sum()

    # rename regions with very little streams (< .01 %) as 'Other'
    streams['region'] = streams.apply(lambda x: x['region'] if x['percent_streams'] >= .01 else 'Other', axis=1)
    # we need another groupby because there are multiple regions with name 'Other'
    streams = streams.groupby('region')['percent_streams'].sum().reset_index().round(3).sort_values(by='percent_streams')
    fig, ax = plt.subplots(figsize=(9,9))
    ax.pie(x=streams['percent_streams'], labels=streams['region'], autopct='%.1f%%')        
    plt.tight_layout()
    st.pyplot()
    
    
if user_menu=='Show number of days a song holds place in Top200':
    #BarChart

    top50 = df[(df['rank'] <= 50)]  # get the top50
    #top50 = top50.drop(['chart'], axis=1).reset_index(drop=True) 
    top50_global = top50[top50['region'] == 'Global']
    n_days = top50_global.groupby(['artist', 'title'])['date'].count().reset_index()
    n_days.columns = ['artist', 'title', 'Number of days in Global Top50']
    plt.figure(figsize=(15,4))
    plt.hist(n_days['Number of days in Global Top50'], bins=50, color ='blueviolet', edgecolor='black', linewidth=1.2)
    plt.yscale('log')
    plt.title('How many days will a song remain on Global Top50 ?')
    plt.xlabel('Number of days in Global Top50')
    plt.ylabel('Number of songs')
    plt.locator_params(axis='x', nbins=25)  # more ticks on x-axis
    plt.show()
    st.pyplot()
    
    
    
if user_menu=='Show Correlation of Rank with Streams':
    top50 = df[(df['rank'] <= 50)]  # get the top50
    #top50 = top50.drop(['chart'], axis=1).reset_index(drop=True) 
    top50_global = top50[top50['region'] == 'Global']
    st.markdown('<p class="big-font"> Correlation of Rank with Streams </p>', unsafe_allow_html=True)
    correlations = [df['streams'].corr(df['rank']) for date, df in top50_global.groupby('date')]
    plt.figure(figsize=(15,4))
    plt.hist(correlations, bins=50, color ='teal', edgecolor='black', linewidth=1.2)
    plt.xlabel('Correlation')
    plt.ylabel('Number of days')
    plt.title('Correlation of rank with streams')
    plt.show()
    st.pyplot()
        
