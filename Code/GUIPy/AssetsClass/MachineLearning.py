import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output
import pandas as pd
import numpy.random as rand
import itertools
import random
from numpy import genfromtxt
import sklearn.model_selection as ms
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn import tree
import sklearn.metrics
import pickle
from sklearn import tree
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

class ActivePrediction:
    def __init__(self):
        self.filename = 'modelwork.sav'
        pass
    def create_model(self, active_path, normal_path, lazy_path):
        
        Active = np.load(active_path, 'r')
        Y_Active = np.ones(len(Active))*2
        SoSoActive = np.load(normal_path, 'r')
        Y_SoSoActive = np.ones(len(SoSoActive))
        Rest = np.load(lazy_path, 'r')
        Y_Rest = np.zeros(len(Rest))
        
        X = np.concatenate(list(map(self.features, [Active, SoSoActive, Rest])), axis=0)
        Y = np.array(np.concatenate((Y_Active, Y_SoSoActive, Y_Rest), axis=0), dtype = int)
        X_train, X_test, Y_train, Y_test =  ms.train_test_split(X, Y, random_state=42, train_size=0.7, shuffle=True)
        lr = RandomForestClassifier()
        lr.fit(X_train, Y_train) 
        pickle.dump(lr, open(self.filename, 'wb'))   

    def features(self, X):
        return np.concatenate((X.mean(axis = 2), X.std(axis = 2), X.min(axis = 2), X.max(axis = 2)), axis=1)
    
    def load_model(self):
        self.model = pickle.load(open(self.filename, 'rb'))
        
    def predict(self, array):
        if (self.model != self.model):
            self.load_model()
        return  self.model.predict(array)
    
    def create_predict_value(self, value):
        value = ap.features(value)
        return (value[0].reshape(1, -1))
        
        
    
    


def features(X):
        return np.concatenate((X.mean(axis = 2), X.std(axis = 2), X.min(axis = 2), X.max(axis = 2)), axis=1)
    


ap = ActivePrediction()
ap.create_model('Logs/active.npy','Logs/normal.npy','Logs/lazy.npy')
ap.load_model()

Check = np.load(f'Logs/active.npy', 'r')
Check = ap.create_predict_value(Check)

print(ap.predict(Check))