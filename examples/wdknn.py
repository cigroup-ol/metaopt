from sklearn.metrics import mean_squared_error as mse
import numpy as np

class KNN:
    def __init__(self, n_neighbors=5, weights=[1.0,1.0,1.0,1.0]):
        self.n_neighbors=n_neighbors
        self.weights=weights

    def fit(self,X,y):
        self.X_train = X
        self.y_train = y

    def dist(self, A,B):
        assert(len(A) == len(B) == len(self.weights))
        l = len(B)
        sum=0.0
        denom=0.0
        for i in range(l):
            sum += (float(A[i])-float(B[i]))**2 * float(self.weights[i])
            denom += float(self.weights[i])
        assert(denom!=0)
        sum /= denom
        return sum

    def predict(self,X):
        res=[]
        for q in X:
            D=[] # list of distances to the train instances
            for t in self.X_train:
                D.append(self.dist(q,t))

            neighbor_labels=self.y_train[np.argsort(D)][0:self.n_neighbors]
            avg = np.mean(neighbor_labels)
            res.append(avg)
        return res

    def score(self,X,y):
        res = self.predict(X)
        return mse(res,y)
