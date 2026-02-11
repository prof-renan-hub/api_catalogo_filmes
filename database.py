import os
import psycopg2



def get_connection():
    conn = psycopg2.connect(
        host= os.environ.get("DB_HOST"),
        database= os.environ.get("DB_NAME"),
        user= os.environ.get("DB_USER"),
        password= os.environ.get("DB_PASSWORD"),
        sslmode= os.environ.get("DB_SSLMODE")
    )
    return conn
    # return psycopg2.connect(
    #     'postgresql://neondb_owner:npg_hnXiLA9QY2db@ep-jolly-firefly-ai6uy2ke-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
    # )
