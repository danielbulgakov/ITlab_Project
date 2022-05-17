from asyncio.windows_events import NULL
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
import os

import AssetsClass.GlobalVariables as gb

class ActivePrediction:
    def __init__(self):
        self.filename = 'Logs/modelwork.sav'
        pass
    def create_model(self, active_path, normal_path, lazy_path):
        
        Active = np.load(active_path, 'r')
        Y_Active = np.ones(len(Active))*2
        SoSoActive = np.load(normal_path, 'r')
        Y_SoSoActive = np.ones(len(SoSoActive))
        Rest = np.load(lazy_path, 'r')
        Y_Rest = np.zeros(len(Rest))
        
        print(Active.shape, SoSoActive.shape, Rest.shape)
        X = np.concatenate(list(map(self.features, [Active, SoSoActive, Rest])), axis=0)
        Y = np.array(np.concatenate((Y_Active, Y_SoSoActive, Y_Rest), axis=0), dtype = int)
        X_train, X_test, Y_train, Y_test =  ms.train_test_split(X, Y, random_state=42, train_size=0.7, shuffle=True)
        lr = RandomForestClassifier()
        lr.fit(X_train, Y_train) 
        pickle.dump(lr, open(self.filename, 'wb'))   

    def features(self, X):
        return np.concatenate((X.mean(axis = 2), X.std(axis = 2), X.min(axis = 2), X.max(axis = 2)), axis=1)
    
    def load_model(self):
        if (not os.path.exists(self.filename)) :
            self.create_model('Logs/active.npy', 'Logs/normal.npy', 'Logs/lazy.npy')

        file = open(self.filename, 'rb')

        self.model = pickle.load(open(self.filename, 'rb'))
        
    def predict(self, array):
        print(array.shape)
        if (self.model != self.model):
            self.load_model()
        return  self.model.predict(array)
    
    def create_predict_value(self, value):
        print(value.shape)
        value = self.features(value)
        return (value[-1].reshape(1, -1))
        
        

class PredictHandler:
    def __init__(self):
        self.ap = ActivePrediction()
        self.ap.load_model()
        pass
    
    def next_predict(self):
        if (gb.asd.get_array().size != 0):
            return self.return_value(self.ap.predict(self.ap.create_predict_value(gb.asd.get_array())))
        return self.return_value([-1])
    
    def return_value(self, listv ):
        if (listv[0] == 0) : return 'Малая активность'
        elif (listv[0] == 1) : return 'Средняя активность'
        elif (listv[0] == 2) : return 'Высокая активность'
        else : return 'Данные отсуствуют'
        
        

    

    


# ap = ActivePrediction()
# ap.create_model('Logs/active.npy','Logs/normal.npy','Logs/lazy.npy')
# ap.load_model()

# Check = np.load(f'Logs/data.npy', 'r')
# print("asdsad", Check[0].shape)
# Check = ap.create_predict_value(Check)

# print(ap.predict(Check))
