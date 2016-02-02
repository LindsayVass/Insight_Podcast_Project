import pandas as pd
from gensim import corpora, models, similarities
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def map_id(podcast_id, id_mapping):
	gensim_id = id_mapping[id_mapping['podcast_id'] == podcast_id].index
	gensim_id = gensim_id[0]
	return gensim_id

def run_search(corpus, lsi, index, gensim_id):
	search_vec = lsi[corpus[gensim_id]]
	sim_scores = index[search_vec]
	sim_df = pd.DataFrame({"similarity" : sim_scores})
	return sim_df

def sim(podcast_id, id_mapping, corpus, lsi, index):
	gensim_id = map_id(podcast_id, id_mapping)
	sim_df = run_search(corpus, lsi, index, gensim_id)
	sim_df = pd.concat([sim_df, id_mapping], axis=1)
	sim_df = sim_df.sort_values('similarity', ascending=False)
	return sim_df