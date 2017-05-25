from pyspark import SparkConf, SparkContext
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating


def parse_data(line):
    fields = line.split("\t")
    return (int(fields[0]), int(fields[1]), float(fields[2]), int(fields[3][-1]))
    
# set up environment
conf = SparkConf() \
        .setAppName("MovieLensALS") \
        .set("spark.executor.memory", "1g")
sc = SparkContext(conf=conf)

ratings = sc.textFile("ml-100k/u.data").map(parse_data)#.filter(lambda x: x is not None)

ratings_train = ratings.filter(lambda x: x[3] < 8)
ratings_test = ratings.filter(lambda x: x[3] >= 8)

ratings_train.count()
ratings_test.count()

model = ALS.train(ratings_train, rank = 10, iterations = 10)

test_data = ratings_test.map(lambda x: (x[0], x[1]))
predictions = model.predictAll(test_data)
ratesAndPreds = ratings_test.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
print("Mean Squared Error = " + str(MSE))

