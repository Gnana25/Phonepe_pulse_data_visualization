#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install mysql.connector')
get_ipython().system('pip install plotly')
get_ipython().system('pip install os')
get_ipython().system('pip install gitpython')


# In[1]:


import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json


# In[2]:


path0 = "C:/Users/LENOVO/Downloads/pulse-master/data/aggregated/transaction/country/india/"
f_df = pd.DataFrame()
f_list=[]
for i in range(2018,2023):
    path=path0+str(i)+"/"
    for j in range(1,5):
        
        path1 = path+str(j)+".json"
        df = pd.read_json(path1)
        st = df.to_json(orient='split')
        u_df = json.loads(st)
        x = u_df['data'][2][2]
        v_list=[]
        for k in range(0,len(x)):
            dict_t={}
            dict_t['transaction_type']=x[k]['name']
            dict_t['year']=i
            dict_t['count'] = x[k]['paymentInstruments'][0]['count']
            dict_t['amount'] = x[k]['paymentInstruments'][0]['amount']
            f_list.append(dict_t)
#print(f_list)
transaction_overall_list = f_list
transaction_overall_df = pd.DataFrame.from_dict(f_list)
display(transaction_overall_df)


# In[ ]:





# In[11]:


path0 = "C:/Users/LENOVO/Downloads/pulse-master/data/aggregated/transaction/country/india/state/"
states = os.listdir(path0)
states
f_list=[]
for i in states:
    path1=path0+str(i)+"/"
    for j in range(2018,2023):
        path2 = path1+str(j)+"/"
        for k in range(1,5):
            path = path2+str(k)+".json"
            df = pd.read_json(path)
            st = df.to_json(orient='split')
            u_df = json.loads(st)['data'][2][2]
            print(len(u_df))
            for l in range(0,len(u_df)):
                dict_t={}
                dict_t['state'] =i
                dict_t['transaction_type']=u_df[l]['name']
                dict_t['year']=j
                dict_t['count'] = u_df[l]['paymentInstruments'][0]['count']
                dict_t['amount'] = u_df[l]['paymentInstruments'][0]['amount']
                print(dict_t)
                f_list.append(dict_t)
transaction_state_wise_df = pd.DataFrame.from_dict(f_list)
display(transaction_state_wise_df)
transaction_state_wise_list = f_list


# In[ ]:





# In[13]:


mydb = sql.connect(host="localhost",
                   user="root",
                   password="",
                   #database= "Phonepe_pulse"
                  )
mycursor = mydb.cursor(buffered=True)


# In[59]:


mycursor.execute("CREATE DATABASE Phonepe_pulse")


# In[77]:


mycursor.execute("USE Phonepe_pulse")


# In[61]:


mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Phonepe_pulse.Transaction_Overall (
        transaction_type VARCHAR(255),
        year VARCHAR(255),
        count VARCHAR(255),
        amount VARCHAR(255)
    )
""")


# In[62]:


mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Phonepe_pulse.Transaction_Statewise (
        state VARCHAR(255),
        transaction_type VARCHAR(255),
        year VARCHAR(255),
        count VARCHAR(255),
        amount VARCHAR(255)
    )
""")


# In[67]:


for x in transaction_overall_list:
    query= 'INSERT INTO Phonepe_pulse.Transaction_Overall (transaction_type,year,count,amount) VALUES (%s,%s,%s,%s)'
    mycursor.execute(query, (x['transaction_type'], x['year'], x['count'],x['amount']))

mydb.commit()


# In[14]:


for x in transaction_state_wise_list:
    query= 'INSERT INTO Phonepe_pulse.Transaction_Statewise (state,transaction_type,year,count,amount) VALUES (%s,%s,%s,%s,%s)'
    mycursor.execute(query, (x['state'],x['transaction_type'], x['year'], x['count'],x['amount']))

mydb.commit()


# In[ ]:


#user table insertion


# In[29]:


path0 = "C:/Users/LENOVO/Downloads/pulse-master/data/aggregated/user/country/india/"
f_df = pd.DataFrame()
f_list=[]
for i in range(2018,2023):
    path=path0+str(i)+"/"
    for j in range(1,5):
        dict_t ={}
        path1 = path+str(j)+".json"
        df = pd.read_json(path1)
        st = df.to_json(orient='split')
        u_df = json.loads(st)
        x = u_df['data'][0][2]['registeredUsers']
        dict_t['year'] = i
        dict_t['users_count'] = x
        f_list.append(dict_t)

user_overall_list = f_list
user_overall_df = pd.DataFrame.from_dict(f_list)
display(user_overall_df)


# In[35]:


path0 = "C:/Users/LENOVO/Downloads/pulse-master/data/aggregated/user/country/india/state/"
states = os.listdir(path0)
states
f_list=[]
for i in states:
    path1=path0+str(i)+"/"
    for j in range(2018,2023):
        path2 = path1+str(j)+"/"
        for k in range(1,5):
            path = path2+str(k)+".json"
            df = pd.read_json(path)
            st = df.to_json(orient='split')
            u_df = json.loads(st)
            #print(u_df['data'][0][2]['registeredUsers'])
            for l in range(0,len(u_df)):
                dict_t={}
                dict_t['state'] =i
                dict_t['users_count']=u_df['data'][0][2]['registeredUsers']
                dict_t['year']=j
                #print(dict_t)
                f_list.append(dict_t)
user_state_wise_df = pd.DataFrame.from_dict(f_list)
display(user_state_wise_df)
user_state_wise_list = f_list


# In[36]:


mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Phonepe_pulse.User_Overall (
        users_count VARCHAR(255),
        year VARCHAR(255)
    )
""")


# In[37]:


mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Phonepe_pulse.User_Statewise (
        state VARCHAR(255),
        users_count VARCHAR(255),
        year VARCHAR(255)
    )
""")


# In[38]:


for x in user_overall_list:
    query= 'INSERT INTO Phonepe_pulse.User_Overall (users_count,year) VALUES (%s,%s)'
    mycursor.execute(query, (x['users_count'], x['year']))
mydb.commit()


# In[39]:


for x in user_state_wise_list:
    query= 'INSERT INTO Phonepe_pulse.User_Statewise (state,users_count,year) VALUES (%s,%s,%s)'
    mycursor.execute(query, (x['state'],x['users_count'], x['year']))

mydb.commit()


# In[ ]:




