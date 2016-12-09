from sklearn.preprocessing import StandardScaler  
from sklearn.decomposition import PCA           
import matplotlib.pyplot as plt


df = pd.read_csv('train_v2.csv')
df = df.dropna(axis = 0)
df = df[df.columns[df.dtypes != 'O']]

sc = StandardScaler() 
X_s = sc.fit_transform(df.values[:, :-1])
X_s = X_s[:, X_s.var(axis = 0) != 0] 
y = df.values[:, -1].reshape(-1, 1)

pca = PCA()
pca.fit(X_s)

plt.plot(pca.explained_variance_ratio_)
plt.yscale('log')
plt.grid(True)
plt.show()

