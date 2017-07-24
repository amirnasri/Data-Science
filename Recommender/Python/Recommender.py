from MF import ExplicitMF, get_mse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_learning_curve(iter_array, model):
    plt.plot(iter_array, model.train_mse, \
             label='Training', linewidth=5)
    plt.plot(iter_array, model.test_mse, \
             label='Test', linewidth=5)


    plt.xticks(fontsize=16);
    plt.yticks(fontsize=16);
    plt.xlabel('iterations', fontsize=30);
    plt.ylabel('MSE', fontsize=30);
    plt.legend(loc='best', fontsize=20);


def train_test_split(ratings):
	test = np.zeros(ratings.shape)
	train = ratings.copy()
	for user in xrange(ratings.shape[0]):
		test_ratings = np.random.choice(ratings[user, :].nonzero()[0],
		                                size=10,
		                                replace=False)
		train[user, test_ratings] = 0.
		test[user, test_ratings] = ratings[user, test_ratings]

	# Test and training are truly disjoint
	assert (np.all((train * test) == 0))
	return train, test


names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('ml-100k/u.data', sep='\t', names=names)

n_users = df.user_id.unique().shape[0]
n_items = df.item_id.unique().shape[0]
ratings = np.zeros((n_users, n_items))
for row in df.itertuples():
    ratings[row[1]-1, row[2]-1] = row[3]



train, test = train_test_split(ratings)

MF_ALS = ExplicitMF(train, n_factors=40, \
                    user_reg=0.0, item_reg=0.0)
print MF_ALS

'''

latent_factors = [5, 10, 20, 40, 80]
regularizations = [0.1, 1., 10., 100.]
regularizations.sort()
iter_array = [1, 2, 5, 10, 25, 50, 100]

best_params = {}
best_params['n_factors'] = latent_factors[0]
best_params['reg'] = regularizations[0]
best_params['n_iter'] = 0
best_params['train_mse'] = np.inf
best_params['test_mse'] = np.inf
best_params['model'] = None

for fact in latent_factors:
    print 'Factors: {}'.format(fact)
    for reg in regularizations:
        print 'Regularization: {}'.format(reg)
        MF_ALS = ExplicitMF(train, n_factors=fact, \
                            user_reg=reg, item_reg=reg)
        MF_ALS.calculate_learning_curve(iter_array, test)
        min_idx = np.argmin(MF_ALS.test_mse)
        if MF_ALS.test_mse[min_idx] < best_params['test_mse']:
            best_params['n_factors'] = fact
            best_params['reg'] = reg
            best_params['n_iter'] = iter_array[min_idx]
            best_params['train_mse'] = MF_ALS.train_mse[min_idx]
            best_params['test_mse'] = MF_ALS.test_mse[min_idx]
            best_params['model'] = MF_ALS
            print 'New optimal hyperparameters'
            print pd.Series(best_params)

best_als_model = best_params['model']
plot_learning_curve(iter_array, best_als_model)

'''











#iter_array = [1, 2, 5, 10, 25, 50, 100]
#MF_ALS.calculate_learning_curve(iter_array, test)
#sns.set()
#plt.figure()
#plot_learning_curve(iter_array, MF_ALS)
#plt.show()

#best_als_model = ExplicitMF(ratings, n_factors=10, learning='als', \
#                            item_fact_reg=0.1, user_fact_reg=0.1)
#best_als_model.train(100)