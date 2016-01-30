from flask import render_template
from flask_podcast import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from flask import request
import preprocess_text as pp


user = 'lindsay' #add your username here (same as previous postgreSQL)            
host = 'localhost'
dbname = 'podcast'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user)
cursor = con.cursor()

@app.route('/')
@app.route('/index')
def index():
  return "Hello, World!"

@app.route('/input')
def podcast_input():
  return render_template("input.html")

@app.route('/check_input')
def podcast_check_input():
  name_query = request.args.get('podcast_name')

  # this line will get used for keyword searching instead of name
  print pp.preprocess_text(name_query)

  query = "SELECT id, name FROM podcast WHERE '%s' %% name;" % name_query
  
  query_results=pd.read_sql_query(query,con)
  
  name_results = []
  for i in range(query_results.shape[0]):
    name_results.append(dict(id=query_results.iloc[i]['id'], name=query_results.iloc[i]['name'].decode('utf-8')))
  return render_template("check_input.html", name_results=name_results)

@app.route('/output')
def podcast_output():
  podcast_id = int(request.args.get('id'))
  
  query = "SELECT podcast_similarity.similarity, podcast.name, podcast.view_url, podcast.artwork_url100 FROM podcast INNER JOIN podcast_similarity ON match_id = podcast.id WHERE search_id='%s' ORDER BY similarity DESC LIMIT 25;"
  
  data = (podcast_id, )

  query_results = pd.read_sql_query(cursor.mogrify(query, data), con)

  podcast_results = []
  for i in range(query_results.shape[0]):
    podcast_results.append(dict(similarity=query_results.iloc[i]['similarity'], name=query_results.iloc[i]['name'].decode('utf-8'), view_url=query_results.iloc[i]['view_url'], artwork_url100=query_results.iloc[i]['artwork_url100']))
  
  query = "SELECT name FROM podcast WHERE id='%s'"
  query_results = pd.read_sql_query(cursor.mogrify(query, data), con)

  return render_template("output.html", podcast_results=podcast_results, search_name=query_results.iloc[0]['name'].decode('utf-8'))

# def index():
#     return render_template("index.html",
#        title = 'Home', user = { 'nickname': 'Miguel' },
#        )

# @app.route('/db')
# def birth_page():
#     sql_query = """                                                             
#                 SELECT * FROM birth_data_table WHERE delivery_method='Cesarean'\
# ;                                                                               
#                 """
#     query_results = pd.read_sql_query(sql_query,con)
#     births = ""
#     print query_results[:10]
#     for i in range(0,10):
#         births += query_results.iloc[i]['birth_month']
#         births += "<br>"
#     return births

# @app.route('/db_fancy')
# def cesareans_page_fancy():
#     sql_query = """
#                SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean';
#                 """
#     query_results=pd.read_sql_query(sql_query,con)
#     births = []
#     for i in range(0,query_results.shape[0]):
#         births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
#     return render_template('cesareans.html',births=births)

# @app.route('/output')
# def cesareans_output():
#   #pull 'birth_month' from input field and store it
#   patient = request.args.get('birth_month')
#     #just select the Cesareans  from the birth dtabase for the month that the user inputs
#   query = "SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean' AND birth_month='%s'" % patient
#   print query
#   query_results=pd.read_sql_query(query,con)
#   print query_results
#   births = []
#   for i in range(0,query_results.shape[0]):
#       births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
#       the_result = ModelIt(patient,births)
#   return render_template("output.html", births = births, the_result = the_result)