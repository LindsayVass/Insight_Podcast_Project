from flask import render_template
from flask_podcast import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from flask import request
from flask import jsonify
import preprocess_text as pp
from simserver import SessionServer
import Pyro4
import html


user = 'lindsay' #add your username here (same as previous postgreSQL)            
host = 'localhost'
dbname = 'podcast'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user)
cursor = con.cursor()

service = Pyro4.Proxy(Pyro4.locateNS().lookup('gensim.testserver'))

def pg_int_array(the_list):
    return '(' + ','.join(the_list) + ')'


@app.route('/')
@app.route('/index')
def index():
  return "Hello, World!"

@app.route('/d3_test')
def d3_test():
  podcast_results = request.args.get('podcast_results')
  print podcast_results
  return(render_template("d3_test.html", podcast_results=podcast_results)

@app.route('/typeahead')
def typeahead_input():
  return render_template("typeahead.html")

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    search = '%' + search.lower() + '%'
    query = "SELECT name, id FROM podcast WHERE lower(name) LIKE '%s';" % search
    matching_results = pd.read_sql_query(query, con)
    matching_results['name'] = [html.escape(x) for x in matching_results['name']]
    matching_results['name'] = [x.decode('utf-8') for x in matching_results['name']]
  
    return matching_results.to_json(None,"records")

@app.route('/input')
def podcast_input():
  # check simserver status
  print(service.status())

  return render_template("input.html")


@app.route('/check_input')
def podcast_check_input():
  name_query = request.args.get('podcast_name')
  name_query = '%' + name_query.lower() + '%'
  # this line will get used for keyword searching instead of name
  #print pp.preprocess_text(name_query)

  query = "SELECT name, id FROM podcast WHERE lower(name) LIKE '%s';" % name_query
  
  query_results=pd.read_sql_query(query,con)
  

  name_results = []
  for i in range(query_results.shape[0]):
    name_results.append(dict(id=query_results.iloc[i]['id'], name=query_results.iloc[i]['name'].decode('utf-8')))
  return render_template("check_input.html", name_results=name_results)


@app.route('/output')
def podcast_output():
  podcast_id = int(request.args.get('id'))

  similarity_results = service.find_similar(str(podcast_id), max_results = 100)

  # remove the searched podcast from list (identity match)
  similarity_results = [i for i in similarity_results if i[0] != str(podcast_id)]

  ids = [x[0] for x in similarity_results]
  query = """
  SELECT name, view_url, artwork_url100, id
  FROM podcast
  WHERE id IN %s;
  """
  query = query.replace('\n', ' ')
  cursor.execute(query % (pg_int_array(ids)))
  query_results = cursor.fetchall()
  
  podcast_results = []
  for i in range(len(query_results)):
    podcast_results.append(dict(similarity=similarity_results[i][1], name=query_results[i][0].decode('utf-8'), view_url=query_results[i][1], artwork_url100=query_results[i][2]))
  
  query = "SELECT name FROM podcast WHERE id='%s'"
  cursor.execute(query % podcast_id)
  podcast_name = cursor.fetchall()
  podcast_name = podcast_name[0][0].decode('utf-8')



  return render_template("output.html", podcast_results=podcast_results, search_name=podcast_name)
