from MediumWebscrapper.medium_webscrapper import web_scrape
import streamlit as st
import pandas as pd
from datetime import datetime
from pytz import timezone
import json
All_topics=['Select Topics','cybersecurity','information-security','blockchain','Cryptocurrency','web3','security',
            'ai','machine-learning','deep-learning','nlp','data-science','data-analysis','image-processing',
            'cloud-computing','cloud-services','dev-ops',
            'android','app-development','flutter',
            'web-development','Software-Development','backend-development','backend']

tag=st.selectbox('Choose the topic',All_topics)
generate_csv=st.button('Generate CSV')
if tag!='Select Topics':
    blogs=web_scrape(tag)
    st.write(f'Number of Blogs Scrapped are {len(blogs)}')
    # Create Json File
    st.code(json.dumps(blogs))
    with open('blogs.json','w') as f:
        f.write(json.dumps(blogs))
    if generate_csv:
        try:
            df=pd.read_json('blogs.json')
            time=datetime.now(timezone("Asia/Kolkata")).date()
            df.to_csv(f'D:/BVM/Sem 6 Work/Mini Project/Blog-Recommendation-System-Notebooks/MediumBlogData/{tag}_mediumblog{time}.csv',index=False)
            st.write('Generated')
        except:
            st.write('Loading....')

#streamlit run MediumWebscrapper.py
