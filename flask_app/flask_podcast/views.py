from flask import render_template
from flask_podcast import app
import pandas as pd
import psycopg2
from flask import request
import preprocess_text as pp
import html
import numpy as np 
from sklearn import manifold
import os
from json import dumps
from gensim import corpora, models, similarities
import get_similarity
from run_mds import run_mds
from flask import jsonify

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_DATA = os.path.join(APP_STATIC, 'data')

# set up database connection
user = 'lindsay'          
host = 'localhost'
dbname = 'podcast'
con = None
con = psycopg2.connect(database = dbname, user = user)
cursor = con.cursor()

# load gensim data
corpus = corpora.MmCorpus(os.path.join(APP_DATA, 'corpus_tfidf.mm'))
lsi = models.LsiModel.load(os.path.join(APP_DATA, 'model.lsi'))
index = similarities.MatrixSimilarity.load(os.path.join(APP_DATA, 'tfidf_lsi_similarities.index'))
id_mapping = pd.read_pickle(os.path.join(APP_DATA, 'podcast_id_to_gensim_id.pkl'))

# load distance matrix
distance_matrix = np.load(os.path.join(APP_DATA, 'distance_matrix.npy'))


def pg_int_array(the_list):
  return '(' + ','.join(the_list) + ')'

def pd_to_json_dict(pd):
  pd = [dict([(colname, row[i]) for i, colname in enumerate(pd.columns)]) for row in pd.values]
  return pd

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
  num_results = 101

  podcast_id = int(request.args.get('id'))
  
  # run similarity analysis
  sim_df = get_similarity.sim(podcast_id, id_mapping, corpus, lsi, index)
  
  # get top results
  top_sim = sim_df.iloc[:num_results,]

  # run mds on top results
  mds_df = run_mds(distance_matrix, top_sim)

  # add variable to identify the searched podcast
  mds_df['searched'] = [False] * mds_df.shape[0]
  mds_df['searched'][mds_df['podcast_id'] == podcast_id] = True
  
  # take top ids
  ids = list(mds_df['podcast_id'].values)
  ids = [str(int(x)) for x in ids]
  ids = ids[:num_results]
  
  # query the db
  query = """
  SELECT name, view_url, artwork_url100, id
  FROM podcast
  WHERE id IN %s;
  """
  query = query.replace('\n', ' ')

  cursor.execute(query % (pg_int_array(ids)))
  query_results = cursor.fetchall()

  # convert to dataframe
  columnNames = ['name', 'view_url', 'artwork_url100', 'id']
  podcast_results = pd.DataFrame(columns=columnNames)
  podcast_results['name'] = [x[0] for x in query_results]
  podcast_results['view_url'] = [x[1] for x in query_results]
  podcast_results['artwork_url100'] = [x[2] for x in query_results]
  podcast_results['id'] = [x[3] for x in query_results]

  # merge with mds data
  merge_results = pd.merge(mds_df, podcast_results, how = 'inner', left_on='podcast_id', right_on='id')

  # convert to jsonlike
  podcast_results = []
  for i in range(num_results):
    podcast_results.append(dict(similarity=merge_results.iloc[i]['similarity'], name=merge_results.iloc[i]['name'].decode('utf-8'), view_url=merge_results.iloc[i]['view_url'], artwork_url100=merge_results.iloc[i]['artwork_url100']))

  podcast_results_no_self = podcast_results[1:]

  del(merge_results['view_url'])
  del(merge_results['artwork_url100'])
  merge_dict = pd_to_json_dict(merge_results)

  # get name of searched podcast
  query = "SELECT name FROM podcast WHERE id='%s'"
  cursor.execute(query % podcast_id)
  podcast_name = cursor.fetchall()
  podcast_name = podcast_name[0][0].decode('utf-8')

  # return render_template("output.html", podcast_results=podcast_results, search_name=podcast_name, pod_ids=pod_ids, mds_data=mds_data)
  return render_template("output.html", podcast_results_no_self=podcast_results_no_self, podcast_results=merge_dict, search_name=podcast_name)
  