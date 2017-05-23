from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating


def parse_data(x):
    try:
        return Rating(int(x[0]), int(x[1]), float(x[2]))
    except ValueError:
        pass

# set up environment
conf = SparkConf() \
        .setAppName("MovieLensALS") \
        .set("spark.executor.memory", "1g")
sc = SparkContext(conf=conf)

ratings = sc.textFile("ml-100k/u.data").map(parse_data).filter(lambda x: x is not None)

als = ALS()

rank = 10
model = als.train(ratings, rank)

test_data = ratings.map(lambda x: (x[0], x[1]))
predictions = model.predictAll(test_data)
