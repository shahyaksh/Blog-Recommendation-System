from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector as SqlConnector

while True:
    try:
        mydb = SqlConnector.connect(host="blog-recommedation-system.cu9zz7jlsnla.ap-south-1.rds.amazonaws.com",
                                    user="yaksh",
                                    password="Yaksh_170802", database="blog_recommendation_system")
        cursor = mydb.cursor()
        print("Connection to Database Successful")
        break
    except Exception as error:
        print("Connection to Database Failed")
        print("Error:", error)
        time.sleep(2)
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)