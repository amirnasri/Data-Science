import pandas as pd
import numpy as np
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import os
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize
import pickle
import sys

ratings = pd.read_csv('ml-100k/u.data', delimiter="\t", engine="python", header=None)
ratings.columns = ["UserID::MovieID::Rating::Timestamp".split("::")]

# Load movie table
movies = pd.read_csv('ml-100k/u.item', delimiter='|', engine='python', header=None)
# Movie table columns as provided in the ReadMe file
columns = ' MovieID | movie title | release date | video release date |' \
              'IMDb URL | unknown | Action | Adventure | Animation |'\
              'Children | Comedy | Crime | Documentary | Drama | Fantasy |'\
              'Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |'\
              'Thriller | War | Western'.split('|')

movies.columns = ["-".join(i.strip().split()) for i in columns]
movies.head()

print "The following movie id's are missing from movie table"
print sorted(set(range(1, movies.MovieID.max())) - set(movies.MovieID))
print "\nnumber of unique movies: %s\n" %  len(set(movies.MovieID))

# movie id have some missing values in addition to the missing values above
# , i.e., there are movies that are not rated by any user.
mi = ratings['MovieID'].unique()
mi.sort()
print "The following movie id's exist in movie table are not rate by any user"
print sorted(set(movies.MovieID) - set(mi))
print len(mi)

# movie-ID: id's provided in the movie table
 # movie-index: index ranges from 0 to #(unique movies) - 1
movie_index_to_ID = dict(zip(range(len(mi)), mi))
movie_ID_to_index = {k: v for v, k in movie_index_to_ID.iteritems()}


# Setting up spark session and spark context
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

sc = spark.sparkContext
sc.setLogLevel("WARN")

# TODO: Should use broadcast for movie_ID_to_index?
def parse_data(line):
	fields = line.split("\t")
	user_id = int(fields[0])
	movie_id = int(fields[1])
	rating = float(fields[2])
	ts = fields[3]
	return movie_ID_to_index_bc.value[movie_id], user_id - 1, rating, ts


movie_ID_to_index_bc = sc.broadcast(movie_ID_to_index)
# u_data_file = os.path.join("ml-1m", "ratings.dat")
u_data_file = os.path.join("ml-100k", "u.data")
ratings_rdd = sc.textFile(u_data_file).map(parse_data)  # .cache().filter(lambda x: x is not None)

ratings_columns = "UserID::MovieID::Rating::Timestamp".split("::")
ratings_sp = spark.createDataFrame(ratings_rdd, schema=ratings_columns)

model = ALS.train(ratings_sp.select(['UserID', 'MovieID', 'Rating']), rank = 10, iterations = 30)


def row_style_to_coordinate(m):
	"""
	Change from row-style to coordinate style matrix:
	m = [
	(0, (v00, v01, v02))
	(2, (v20, v21, v22))
	(5, (v50, v51, v52))
	]

	=>

	[
	(0, [(0, v00), (1, v01), (2, v02)])
	(2, [(0, v20), (1, v21), (2, v22)])
	(5, [(0, v50), (1, v51), (2, v52)])
	]

	=>

	[
	(0, 0, v00), (0, 1, v01), (0, 2, v02),
	(2, 0, v20), (2, 1, v21), (2, 2, v22),

	]
	"""
	x = m.map(lambda r: (r[0], zip(range(len(r[1])), r[1])))
	return x.flatMap(lambda r: [(r[0], i[0], i[1]) for i in r[1]])

def coordinate_to_sparse(m):
    row, col, data = np.array(m).T
    return csr_matrix((data, (row, col)))

pf_rdd = model.productFeatures()
uf_rdd = model.userFeatures()
user_features = row_style_to_coordinate(pf_rdd)
product_features = row_style_to_coordinate(uf_rdd)
#print coordinate_to_sparse(user_features.collect()).todense().shape
#print coordinate_to_sparse(product_features.collect()).todense().shape

pf_sparse = coordinate_to_sparse(product_features.collect())
pf = np.array(pf_sparse.todense())


pf_norm = normalize(pf, axis=1)

pp_sim = np.dot(pf_norm, pf_norm.T)

recom_movie_index = np.argsort(pp_sim[0, :])[::-1][:10]

recom_movie_df = pd.merge(pd.DataFrame({'MovieID':[movie_index_to_ID[i] for i in recom_movie_index]}), movies, how='inner', on='MovieID', suffixes=('_x', '_y'))

print recom_movie_df

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

srv_data_folder = './data'
if len(sys.argv) > 1:
	srv_data_folder = sys.argv[1]
curr_dir = os.getcwd()
os.chdir(srv_data_folder)
movies.to_pickle('movies_df.pkl')
save_obj(movie_index_to_ID, 'movie_index_to_ID')
np.save('pp_sim', pp_sim)
os.chdir(curr_dir)
