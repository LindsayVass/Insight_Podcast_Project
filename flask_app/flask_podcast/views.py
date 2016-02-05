from flask import render_template, request
from flask_podcast import app
import pandas as pd
import psycopg2
import preprocess_text as pp
import html
import numpy as np 
from sklearn import manifold
import os
from json import dumps
from gensim import corpora, models, similarities
import get_similarity
from run_mds import run_mds

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
dictionary = corpora.Dictionary.load(os.path.join(APP_DATA, 'dictionary.dict'))

# load distance matrix
distance_matrix = np.load(os.path.join(APP_DATA, 'distance_matrix.npy'))

# load PCA data
pca_df = pd.read_pickle(os.path.join(APP_DATA, 'pca_df.pkl'))


def pg_int_array(the_list):
  return '(' + ','.join(the_list) + ')'

def pd_to_json_dict(pd):
  pd = [dict([(colname, row[i]) for i, colname in enumerate(pd.columns)]) for row in pd.values]
  return pd

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError





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

@app.route('/keyword_output', methods=['GET'])
def keyword_output():
  search = request.args.get('keyword')
  pp_search = pp.preprocess_text(search)
  
  pp_dict = dictionary.doc2bow(pp_search)

  search_vec = lsi[pp_dict]

  sim_scores = index[search_vec]
  sim_df = pd.DataFrame({"similarity" : sim_scores})
  sim_df = pd.concat([sim_df, id_mapping], axis=1)
  sim_df = sim_df.sort_values('similarity', ascending=False)

  # take top ids
  num_results=100
  ids = list(sim_df['podcast_id'].values)
  ids = [str(int(x)) for x in ids]
  ids = ids[:num_results]
  
  # query the db
  query = """
  SELECT name, view_url, artwork_url100, id, raw_summary
  FROM podcast
  WHERE id IN %s;
  """
  query = query.replace('\n', ' ')

  cursor.execute(query % (pg_int_array(ids)))
  query_results = cursor.fetchall()

  # convert to dataframe
  columnNames = ['name', 'view_url', 'artwork_url100', 'id', 'summary']
  podcast_results = pd.DataFrame(columns=columnNames)
  podcast_results['name'] = [x[0] for x in query_results]
  podcast_results['view_url'] = [x[1] for x in query_results]
  podcast_results['artwork_url100'] = [x[2] for x in query_results]
  podcast_results['id'] = [x[3] for x in query_results]
  podcast_results['summary'] = [x[4] for x in query_results]

  # merge with pca data
  table_results = pd.merge(sim_df, podcast_results, how = 'inner', left_on='podcast_id', right_on='id')
  scatter_results = table_results.copy(deep=True)


  # convert to jsonlike
  podcast_results = []
  for i in range(num_results):
    podcast_results.append(dict(similarity=table_results.iloc[i]['similarity'], name=table_results.iloc[i]['name'].decode('utf-8'), view_url=table_results.iloc[i]['view_url'], artwork_url100=table_results.iloc[i]['artwork_url100'], id=table_results.iloc[i]['id']))

  scatter_results['name'] = [str(x).replace('"', "'") for x in scatter_results['name']]
  scatter_results['summary'] = [str(x).replace('"', "'") for x in scatter_results['summary']]
  scatter_results['summary'] = [x.decode('utf-8') for x in scatter_results['summary']]
  
  merge_dict = pd_to_json_dict(scatter_results)


  return render_template("output_force_layout.html", podcast_results_no_self=podcast_results, podcast_results=merge_dict, search_name=search)

@app.route('/output')
def podcast_output():
  num_results = 101

  podcast_id = int(request.args.get('id'))
  
  # run similarity analysis
  sim_df = get_similarity.sim(podcast_id, id_mapping, corpus, lsi, index)

  # add variables to identify searched and top
  sim_df['searched'] = [False] * sim_df.shape[0]
  sim_df['searched'][sim_df['podcast_id'] == podcast_id] = True
  sim_df['top'] = [False] * sim_df.shape[0]
  sim_df.loc[:num_results, 'top'] = True

  # add PCA coordinates
  sim_df = sim_df.join(pca_df, how='inner')

  # sort by similarity
  sim_df = sim_df.sort(columns='similarity', ascending=False)
  
  # get top results
  # top_sim = sim_df.iloc[:num_results,]


  # run mds on top results
  # mds_df = run_mds(distance_matrix, top_sim)


  # add variable to identify the searched podcast
  # mds_df['searched'] = [False] * mds_df.shape[0]
  # mds_df['searched'][mds_df['podcast_id'] == podcast_id] = True
  
  # take top ids
  ids = list(sim_df['podcast_id'].values)
  ids = [str(int(x)) for x in ids]
  ids = ids[:num_results]
  
  # query the db
  query = """
  SELECT name, view_url, artwork_url100, id, raw_summary
  FROM podcast
  WHERE id IN %s;
  """
  query = query.replace('\n', ' ')

  cursor.execute(query % (pg_int_array(ids)))
  query_results = cursor.fetchall()

  # convert to dataframe
  columnNames = ['name', 'view_url', 'artwork_url100', 'id', 'summary']
  podcast_results = pd.DataFrame(columns=columnNames)
  podcast_results['name'] = [x[0] for x in query_results]
  podcast_results['view_url'] = [x[1] for x in query_results]
  podcast_results['artwork_url100'] = [x[2] for x in query_results]
  podcast_results['id'] = [x[3] for x in query_results]
  podcast_results['summary'] = [x[4] for x in query_results]

  # merge with pca data
  table_results = pd.merge(sim_df, podcast_results, how = 'inner', left_on='podcast_id', right_on='id')
  scatter_results = table_results.copy(deep=True)


  # convert to jsonlike
  podcast_results = []
  for i in range(num_results):
    podcast_results.append(dict(similarity=table_results.iloc[i]['similarity'], name=table_results.iloc[i]['name'].decode('utf-8'), view_url=table_results.iloc[i]['view_url'], artwork_url100=table_results.iloc[i]['artwork_url100'], id=table_results.iloc[i]['id']))

  podcast_results_no_self = podcast_results[1:]

  #print scatter_results.head()

  scatter_results['name'] = [str(x).replace('"', "'") for x in scatter_results['name']]
  scatter_results['summary'] = [str(x).replace('"', "'") for x in scatter_results['summary']]
  scatter_results['summary'] = [x.decode('utf-8') for x in scatter_results['summary']]
  
  merge_dict = pd_to_json_dict(scatter_results)

  # get name of searched podcast
  query = "SELECT name FROM podcast WHERE id='%s'"
  cursor.execute(query % podcast_id)
  podcast_name = cursor.fetchall()
  podcast_name = podcast_name[0][0].decode('utf-8')


  # return render_template("output.html", podcast_results_no_self=podcast_results_no_self, podcast_results=merge_dict, search_name=podcast_name)
  return render_template("output_force_layout.html", podcast_results_no_self=podcast_results_no_self, podcast_results=merge_dict, search_name=podcast_name)