import os
import sys
import numpy as np
from pyspark import SparkConf, SparkContext
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating


def cv_generator(data):
	for i in range(10):
		train = data.filter(lambda x: x[3] != i).map(lambda x: x[:-1])
		test = data.filter(lambda x: x[3] == i).map(lambda x: x[:-1])
		yield train, test 

def parse_data(line):
    fields = line.split("::")
    tup =  (int(fields[0]), int(fields[1]), float(fields[2]), int(fields[3][-1]))
    return tup

# set up environment
if not hasattr(sys, "ps1"):
    conf = SparkConf() \
            .setAppName("MovieLensALS") \
            .set("spark.executor.memory", "1g")
    sc = SparkContext(conf=conf)

sc.setLogLevel("WARN")
#logger = sc._jvm.org.apache.log4j
#logger.LogManager.getLogger("org"). setLevel( logger.Level.ERROR )
#logger.LogManager.getLogger("akka").setLevel( logger.Level.ERROR )

dir = "ml-1m"
if len(sys.argv) >= 2:
	dir = sys.argv[1]

u_data_file = os.path.join(dir, "ratings.dat")
ratings = sc.textFile(u_data_file).map(parse_data).cache()#.filter(lambda x: x is not None)

#ratings_train = ratings.filter(lambda x: x[3] < 8).map(lambda x: x[:-1])
#ratings_test = ratings.filter(lambda x: x[3] >= 8).map(lambda x: x[:-1])

#print("number of train points: %d" % ratings_train.count())
#print("number of test points: %d" % ratings_test.count())

MSE = np.zeros(10)
for i, (ratings_train, ratings_test) in enumerate(cv_generator(ratings)):
    
	model = ALS.train(ratings_train, rank = 10, iterations = 10)

	test_data = ratings_test.map(lambda x: (x[0], x[1]))
	predictions = model.predictAll(test_data).map(lambda r: ((r[0], r[1]), r[2]))
	ratesAndPreds = ratings_test.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
	MSE[i] = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()

	print("Mean Squared Error = " + str(MSE))

