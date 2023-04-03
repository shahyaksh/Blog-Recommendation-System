import mysql.connector as SqlConnector
import pandas as pd
import numpy as np
import nltk
import re
import json
import requests
from nltk import corpus
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

lst_stopwords=corpus.stopwords.words('english')
def pre_process_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
    text=str(text).lower()
    text=text.strip()
    text = re.sub(r'[^\w\s]', '', text)
    lst_text = text.split()
    if lst_stopwords is not None:
        lst_text=[word for word in lst_text if word not in lst_stopwords]
    if flg_lemm:
        lemmatizer = WordNetLemmatizer()
        lst_text = [lemmatizer.lemmatize(word) for word in lst_text]
    if flg_stemm:
        stemmer = PorterStemmer()
        lst_text = [stemmer.stem(word) for word in lst_text]
    text=" ".join(lst_text)
    return text

def get_similar_blog(blogs:dict,ratings:dict):
    blogs_df=pd.DataFrame(blogs)
    blogs_df['clean_blog_content'] = blogs_df['content'].apply(
                                    lambda x: pre_process_text(x,flg_lemm=True,lst_stopwords=lst_stopwords))

    count_vec = CountVectorizer()
    similarity_matrix = count_vec.fit_transform(blogs_df['clean_blog_content'])
    cosine_sim = cosine_similarity(similarity_matrix)

    ratings_df = pd.DataFrame(ratings)
    blogs_to_consider = ratings_df[ratings_df['rating'] == 5]['blog_id']
    high_rated_blogs = blogs_to_consider.values
    rated_blogs = blogs_df[blogs_df['blog_id'].isin(high_rated_blogs)]
    recommended_blogs = []
    recommended_blogs = []
    for blog_id in high_rated_blogs:
        temp_id = blogs_df[blogs_df['blog_id'] == blog_id].index.values[0]
        temp_blog_id = blogs_df[cosine_sim[temp_id] > 0.3]['blog_id'].index.values
        for b_id in temp_blog_id:
            if b_id not in recommended_blogs:
                recommended_blogs.append(b_id)
    return recommended_blogs


