import mysql.connector as SqlConnector
import time
from datetime import datetime
while True:
    try:
        mydb = SqlConnector.connect(host="localhost",
                                    user="root",
                                    password="Yaksh_170802", database="blog_recommendation_system")
        cursor = mydb.cursor(buffered=True)
        print("Connection to Database Successful")
        break
    except Exception as error:
        print("Connection to Database Failed")
        print("Error:", error)
        time.sleep(2)

def get_author_id(author_name:str,blog_name:str):
    cursor.execute("select * from author where author_name=%s", [author_name])
    auth_details = cursor.fetchone()
    Author_id=0
    if auth_details is not None:
        Author_id = auth_details[0]
    else:
       Author_id=add_author(author_name,blog_name)
    return Author_id


def add_author(author_name:str,blog_name:str):
    cursor.execute("""insert into author(author_name,blog_web_name) values(%s,%s)""",(author_name,blog_name))
    mydb.commit()
    cursor.execute("select author_id from author where author_name=%s", [author_name])
    Author_id = cursor.fetchone()[0]
    return Author_id



def insert_blog_in_db(blog:dict):
    if '.' in blog['timestamp']:
        blog['timestamp']=blog['timestamp'].split('.')[0]
    cursor.execute("""select * from blogs where blog_title=%s """,[blog['blog_title']])
    blog_det = cursor.fetchone()
    if blog_det is not None:
        return 'Already Exist'
    else:
        datetime_obj = datetime.strptime(blog['timestamp'],'%Y-%m-%d %H:%M:%S')
        cursor.execute("""insert into blogs(author_id,blog_title,blog_content,blog_link,blog_img,topic,time_stamp)
                          values(%s,%s,%s,%s,%s,%s,%s)""",(blog['author_id'],blog['blog_title'],
                                                                           blog['blog_content'],blog['blog_link'],
                                                                           blog['blog_img'],blog['blog_topic'],
                                                                           datetime_obj
                                                                           ))
        mydb.commit()
        return 'inserted'
