import pandas as pd
from sqlalchemy import create_engine
import MySQLdb

connection_string = 'mysql://readonlyuser:sdnv29b9nOASknc2eivn29bv@82.146.48.79/merch-server'
engine = create_engine(connection_string)
#conn = MySQLdb.Connect( host="82.146.48.79", user = "readonlyuser", db='merch-server',passwd = "sdnv29b9nOASknc2eivn29bv", charset = "UTF8" )

#pip install mysqlclient
sql_query = 'SELECT title FROM productList where productListId=339'
df = pd.read_sql(sql_query, engine)
df = pd.io.sql.read_sql(sql_query, engine)
df.to_json(r'e:/db_export.json', orient='records', force_ascii=False)