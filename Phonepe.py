import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
import pydeck as pdk
import numpy as np 
from streamlit_option_menu import option_menu
from PIL import Image
st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By GNANAVEL T",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Gnanavel*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")
mydb = sql.connect(
  host="localhost",
  user="root",
  password="" ,
  port="3306"
)
print(mydb)
mycursor = mydb.cursor(buffered=True) 
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
if selected == "Home":
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state & district and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, based on Total phonepe users and their app opening frequency.
                """,icon="🔍"
                )
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([2,2,2],gap="large")
        
        with col1:
            st.markdown("### :violet[Transaction count]")
            mycursor.execute("""SELECT DISTINCT state, SUM(count) AS Total_Transactions_Count
                 FROM phonepe_pulse.transaction_statewise
                 GROUP BY count
                 ORDER BY count desc
                 LIMIT 10""")

            df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'count'])
            fig = px.pie(df, values='count',
                             names='state',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['count'],
                             labels={'count':'count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

            with col2:
                 st.markdown("### :violet[Total Transaction Value]")
            mycursor.execute("""SELECT DISTINCT state, SUM(amount) AS Total_Transactions_Amount
                 FROM phonepe_pulse.transaction_statewise
                 GROUP BY amount
                 ORDER BY amount desc
                 LIMIT 10""")

            df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'amount'])
            fig = px.pie(df, values='amount',
                             names='state',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['amount'],
                             labels={'amount':'amount'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

            with col3:
                 st.markdown("### :violet[Type Of Transaction]")
            mycursor.execute("""SELECT DISTINCT transaction_type, SUM(amount) AS Total_Transactions_Amount
                 FROM phonepe_pulse.transaction_overall
                 GROUP BY amount
                 ORDER BY amount desc
                 LIMIT 5""")

            df = pd.DataFrame(mycursor.fetchall(), columns=['transaction_type', 'amount'])
            fig = px.pie(df, values='amount',
                             names='transaction_type',
                             title='Top 4',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['amount'],
                             labels={'amount':'amount'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

# Top Charts - USERS  
    if Type == "Users":
        col1,col2 = st.columns([2,2],gap="small")

        with col1:
            st.markdown("### :violet[Users Count vs Year]")
            mycursor.execute("""SELECT DISTINCT year, SUM(users_count) AS Total_Users
                 FROM phonepe_pulse.user_overall
                 GROUP BY users_count
                 ORDER BY users_count desc""")

            df = pd.DataFrame(mycursor.fetchall(), columns=['year', 'users_count'])
            fig = px.pie(df, values='users_count',
                             names='year',
                             title='Top 5',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['users_count'],
                             labels={'users_count':'users_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("### :violet[Users Count vs State]")
            mycursor.execute("""SELECT DISTINCT state, SUM(users_count) AS Total_Users_of_each_state
                 FROM phonepe_pulse.user_statewise
                 GROUP BY users_count
                 ORDER BY users_count desc
                 LIMIT 15""")

            df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'users_count'])
            fig = px.pie(df, values='users_count',
                             names='state',
                             title='Top 15',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['users_count'],
                             labels={'users_count':'users_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
# MENU 3 - EXPLORE DATA
if selected == "Explore Data":  
    year = st.sidebar.slider("**year**", min_value=2018, max_value=2022)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)   
        # EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute("""SELECT DISTINCT state, sum(count) as Total_Transactions, sum(amount) as Total_amount
                             FROM phonepe_pulse.transaction_statewise 
                             GROUP BY state
                             ORDER BY state
                             """)
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            #df2 = pd.read_json('C:\\Users\\LENOVO\\Downloads\\pulse-master\\data\\map\\transaction\\hover\\country\\india\\state.json')
            #df1.State = df2
            st.write(df1)
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            latitude = [10.7449,15.9129,28.2180,26.2006,25.9644,30.7333,21.2787,20.3974,28.7041,15.2993,22.6708,29.0588,32.1024,33.2778,23.6913,15.3173,10.1632,34.2268,10.5667,22.9734,19.7515,24.6637,25.4670,23.1645,26.1584,20.2376,11.9416,31.1471,27.0238,27.3516,11.1271,18.1124,23.5639,30.0668,27.5706,22.9868]
            longitude =[92.5000,79.7400,94.7278,92.9376,85.2722,76.7794,81.8661,72.8328,77.1025,74.1240,71.5724,76.0856,77.5619,75.3412,85.2722,75.7139,76.6413,77.5619,72.6417,78.6569,75.7139,93.9063,91.3662,92.9376,94.5624,84.2700,79.8083,75.3412,74.2179,88.3239,78.6569,79.0193,91.6761,79.0193,80.0982,87.8550]
            df1['latitude'] = latitude
            df1['longitude'] = longitude
            st.map(data=df1, latitude=latitude, longitude=longitude, size=1000, color='#0000FF', zoom=None, use_container_width=True)
      