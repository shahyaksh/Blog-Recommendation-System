import pandas as pd
from app import cursor, get_user_ratings_in_json_format,ratings_df,rating_path
import numpy as np
import tensorflow as tf
from recommenders.models.rbm.rbm import RBM
from recommenders.datasets.sparse import AffinityMatrix
from recommenders.datasets.python_splitters import numpy_stratified_split
from pytz import timezone
from datetime import datetime
import os
import pathlib


blog_data_2 = pd.read_csv(os.path.abspath("BlogData/blog_data.csv"))
model_path = os.path.join(os.getcwd(), "model/")
top_k_df = pd.read_csv(os.path.join(os.getcwd(), "RecommendedBlogs/top_k_reco.csv"))
old_datetime = top_k_df['timestamp'].values[0]
# Get the user ratings
curr_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
datetime_obj = datetime.strptime(curr_time,'%Y-%m-%d %H:%M:%S')
cursor.execute("SELECT * FROM ratings where timestamp between %s and %s", (old_datetime, datetime_obj))
ratings_list = cursor.fetchall()

if ratings_list == []:
    print("No new ratings")
else:
    # Get the user ratings
        # Convert the ratings into a dataframe
    ratings_json = get_user_ratings_in_json_format(ratings_list)
    ratings_df_new = pd.DataFrame(ratings_json, index=None)
    ratings_df_new.drop(columns=['timestamp'], inplace=True)
    ratings_df = pd.concat([ratings_df, ratings_df_new])
    print(ratings_df.shape)
    ratings_df.drop_duplicates(inplace=True)
    ratings_df.to_csv(rating_path, index=False)
    header = {
        "col_user": "userId",
        "col_item": "blog_id",
        "col_rating": "ratings",
    }

    # generate the affinity matrix
    affinity_matrix = AffinityMatrix(df=ratings_df, **header)
    # obtain the sparse matrix
    X, _, _ = affinity_matrix.gen_affinity_matrix()
    print(X.shape)
    X_train, X_test = numpy_stratified_split(X)
    physical_devices = tf.config.list_physical_devices('GPU')
    print(physical_devices)
    if physical_devices:
        try:
            tf.config.experimental.set_memory_growth(physical_devices[0], True)
        except:
            pass
    with tf.device('/gpu:0'):
        # Initialize the model
        model = RBM(possible_ratings=np.setdiff1d(np.unique(X_train), np.array([0])),
                    visible_units=X_train.shape[1],
                    hidden_units=1200,
                    training_epoch=30,
                    minibatch_size=350,
                    keep_prob=0.7,
                    with_metrics=True)
        model.load(model_path+'rbm_model_V4.ckpt')
        model.fit(X_train)

    K = 10
    # Model prediction on dataset X.
    top_k_1m = model.recommend_k_items(X_test, K)
    predicted_df = pd.DataFrame(data=top_k_1m)

    top_k_df = affinity_matrix.map_back_sparse(top_k_1m, kind='prediction')
    test_df = affinity_matrix.map_back_sparse(X_test, kind='ratings')
    top_k_df['prediction'].fillna(0, axis=0, inplace=True)
    final_topics = []
    for blog in top_k_df['blog_id'].tolist():
        final_topics.append(blog_data_2[blog_data_2['blog_id'] == blog]['topic'].values)
    top_k_df['topic'] = pd.DataFrame(final_topics)

    rated_blog_topics = []
    for blog in ratings_df['blog_id'].tolist():
        rated_blog_topics.append(blog_data_2[blog_data_2['blog_id'] == blog]['topic'].values)
    ratings_df['topic'] = pd.DataFrame(rated_blog_topics)
    model.save(model_path+'rbm_model_V4.ckpt')
    top_k_df['timestamp'] = datetime_obj
    top_k_df.to_csv('top_k_reco.csv', index=False)





