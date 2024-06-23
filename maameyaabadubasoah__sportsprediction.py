# -*- coding: utf-8 -*-
"""MaameYaaBaduBasoah._SportsPrediction

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/177TM-LABqFl2xkhpKYEtvSFZqSjyKo6K
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import os
from sklearn import tree, metrics
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import VotingRegressor
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import joblib

"""**Mounting from Google Drive**"""

from google.colab import drive
drive.mount('/content/drive')

mplayers = pd.read_csv('/content/drive/My Drive/players/male_players (legacy).csv')

pd.set_option('display.max_columns', None)

mplayers.info()

mplayers.head()

"""**Data preprocessing**"""

features_to_select = ['mentality_composure', 'attacking_volleys', 'goalkeeping_reflexes', 'goalkeeping_kicking',
                      'attacking_short_passing', 'dribbling', 'power_stamina', 'defending_standing_tackle',
                      'goalkeeping_positioning', 'movement_reactions', 'attacking_heading_accuracy',
                      'attacking_crossing', 'movement_sprint_speed', 'physic', 'goalkeeping_diving',
                      'defending_sliding_tackle', 'attacking_finishing', 'defending_marking_awareness',
                      'skill_ball_control', 'power_shot_power', 'potential', 'goalkeeping_handling',
                      'movement_balance', 'mentality_penalties', 'mentality_positioning', 'shooting', 'skill_fk_accuracy',
                      'mentality_aggression', 'age', 'power_strength', 'skill_curve',
                      'defending', 'movement_agility', 'height_cm', 'mentality_vision', 'skill_long_passing',
                      'goalkeeping_speed', 'mentality_interceptions', 'weight_kg', 'movement_acceleration', 'overall',
                      'skill_dribbling', 'pace', 'passing', 'power_long_shots']

corr_matrix = mplayers[features_to_select].corr()
corr_matrix['overall'].sort_values(ascending=False)

selected_cols = ['physic', 'goalkeeping_reflexes', 'goalkeeping_positioning', 'potential', 'shooting',
                 'goalkeeping_speed', 'attacking_volleys', 'mentality_interceptions', 'goalkeeping_handling',
                 'attacking_short_passing', 'mentality_vision', 'mentality_positioning', 'movement_reactions',
                 'goalkeeping_kicking', 'skill_fk_accuracy', 'mentality_composure', 'mentality_penalties',
                 'defending', 'skill_long_passing', 'attacking_crossing', 'mentality_aggression', 'goalkeeping_diving',
                 'age', 'power_long_shots', 'skill_curve', 'dribbling', 'attacking_finishing', 'skill_dribbling',
                 'movement_agility', 'power_shot_power', 'skill_ball_control', 'passing']

mplayers = pd.read_csv('/content/drive/My Drive/players/male_players (legacy).csv', usecols = selected_cols)
mplayers.info()

mplayers.fillna(0, inplace=True)

"""Feature Engineering"""

mplayers= mplayers.astype(int)
catching = ['goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking',
                          'goalkeeping_positioning', 'goalkeeping_reflexes', 'goalkeeping_speed']
imputer = SimpleImputer(strategy='mean')
mplayers[catching] = imputer.fit_transform(mplayers[catching])
mplayers['catching'] = mplayers[catching].mean(axis=1)
mplayers.drop(columns=catching, inplace=True)


mentality = ['mentality_interceptions', 'mentality_composure', 'mentality_positioning',
                        'mentality_aggression',  'mentality_penalties', 'mentality_vision']
imputer = SimpleImputer(strategy='mean')
mplayers[mentality] = imputer.fit_transform(mplayers[mentality])
mplayers['mentality'] = mplayers[mentality].mean(axis=1)
mplayers.drop(columns=mentality, inplace=True)


ballskills = ['skill_dribbling', 'skill_long_passing', 'skill_curve', 'skill_fk_accuracy','skill_ball_control']
mplayers['ballskills'] = mplayers[ballskills].mean(axis=1)
mplayers.drop(columns=ballskills, inplace=True)

mplayers.info()

shooting_cols = ['shooting', 'power_long_shots', 'power_shot_power', 'attacking_finishing', 'attacking_volleys']
mplayers['shooting_avg'] = mplayers[shooting_cols].mean(axis=1)
mplayers.drop(columns=shooting_cols, inplace=True)
mplayers.rename(columns={'shooting_avg': 'shooting'}, inplace=True)

passing_cols = ['passing', 'attacking_crossing', 'attacking_short_passing', 'movement_reactions']
mplayers['passing_avg'] = mplayers[passing_cols].mean(axis=1)
mplayers.drop(columns=passing_cols, inplace=True)
mplayers.rename(columns={'passing_avg': 'passing'}, inplace=True)

mplayers.info()

"""Training

"""

y = mplayers['overall']
x = mplayers.drop('overall', axis=1)

sc = StandardScaler()
scaled = sc.fit_transform(x)

x=pd.DataFrame(scaled, columns=x.columns)

xtrain, xtest, Ytrain, Ytest = train_test_split(x, y, test_size= 0.1, random_state=42, stratify=y)

xtrain.shape

"""Training with XGB_REGRESSOR"""

xgb = XGBRegressor()

xgb.fit(xtrain, Ytrain)

xgb_ypred = xgb.predict(xtest)
xgbabsolute_err = mean_absolute_error(xgb_ypred, Ytest)
xgbabsolute_err

"""Training with RANDOM FOREST REGRESSOR"""

rfg=RandomForestRegressor()

rfg.fit(xtrain, Ytrain)
rfg_ypred =rfg.predict(xtest)
rfg_ypred

rfgabsolute_err = mean_absolute_error(rfg_ypred,Ytest)
rfgabsolute_err

"""Training with GRADIENT BOOST REGRESSOR"""

gbr = GradientBoostingRegressor()

gbr.fit(xtrain, Ytrain)
gbr_ypred = gbr.predict(xtest)

gbrabsolute_err = mean_absolute_error(gbr_ypred, Ytest)
gbrabsolute_err

"""Cross-Validation"""

# The hyperparameters for Random Forest Regressor and for Gradient Boost Regressor are:

parameters_rfg = {
    'n_estimators': [10, 15, 20],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 6, 10]
}
parameters_gbr = {
    'n_estimators': [10, 15, 20],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.1, 0.01, 0.001]
}

rfg_gridsearch = GridSearchCV(estimator = RandomForestRegressor(), param_grid = parameters_rfg, scoring = 'neg_mean_absolute_error', cv=5)
rfg_gridsearch.fit(xtrain, Ytrain)
best_rfg = rfg_gridsearch.best_estimator_

gbr_gridsearch = GridSearchCV(estimator = GradientBoostingRegressor(), param_grid = parameters_gbr, scoring = 'neg_mean_absolute_error', cv=5)
gbr_gridsearch.fit(xtrain, Ytrain)
best_gbr = gbr_gridsearch.best_estimator_

bestrfg_ypred = best_rfg.predict(xtest)
best_rfg_abserr = mean_absolute_error(bestrfg_ypred, Ytest)
print("The mean absolute error for the best Random Forest Model is: ", best_rfg_abserr)

bestgbr_ypred = best_gbr.predict(xtest)
best_gbr_abserr = mean_absolute_error(bestgbr_ypred, Ytest)
print("The mean absolute error for the best Gradient Boost Regressor is: ", best_gbr_abserr)

"""The ENSEMBLE MODEL using the Random Forest Regressor and Gradient Boost Regressor models above"""

ensemblemodel = VotingRegressor(estimators=[('rfg', rfg), ('gbr', gbr)])

ensemblemodel.fit(xtrain, Ytrain)
ensemblepredictions = ensemblemodel.predict(xtest)

ensemble_abserr = mean_absolute_error(ensemblepredictions, Ytest)
ensemblepredictions
xtest
Ytest

print("Mean absolute error for Random Forest: ", mean_absolute_error(rfg_ypred, Ytest))
print("Mean absolute error for Gradient Boost Regressor: ", best_gbr_abserr)
print("Mean absolute error for Ensemble Model: ", ensemble_abserr)

stdeviation = np.std(ensemblepredictions)
meanprediction = np.mean(ensemblepredictions)
print("The standard deviation is:", stdeviation)
print("The mean prediction is:", meanprediction)

# creation of the confidence level and margin of error
conf_level = 0.95
z_score = norm.ppf((1 + conf_level)/2)
margin_error = z_score *(stdeviation/np.sqrt(len(ensemblepredictions)))

ubound = meanprediction + margin_error
lbound = meanprediction - margin_error
conf_percentage = ((1-2 * (1 - conf_level)) * 100)

print("The lower bound for the regressors is:", lbound)
print("The upper bound for the regressors is:", ubound)
print("The margin of error for the regressors:", margin_error)
print("The confidence percentage for the regressors is:", conf_percentage)

"""Training with the new Dataset(players22)

"""

players2 = pd.read_csv('/content/drive/My Drive/players/players_22-1.csv', usecols =selected_cols)

players2.fillna(0, inplace=True)

players2= players2.astype(int)

catching = ['goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking',
                          'goalkeeping_positioning', 'goalkeeping_reflexes', 'goalkeeping_speed']
imputer = SimpleImputer(strategy='mean')
players2[catching] = imputer.fit_transform(players2[catching])
players2['goalkeeping'] = players2[catching].mean(axis=1)
players2.drop(columns=catching, inplace=True)


mentality = ['mentality_interceptions', 'mentality_composure', 'mentality_positioning',
                        'mentality_aggression',  'mentality_penalties', 'mentality_vision']
imputer = SimpleImputer(strategy='mean')
players2[mentality] = imputer.fit_transform(players2[mentality])
players2['mentality_att'] = players2[mentality].mean(axis=1)
players2.drop(columns=mentality, inplace=True)


ballskills = ['skill_dribbling', 'skill_long_passing', 'skill_curve', 'skill_fk_accuracy','skill_ball_control']
players2['goodballskills'] = players2[ballskills].mean(axis=1)
players2.drop(columns=ballskills, inplace=True)

shooting_cols = ['shooting', 'power_long_shots', 'power_shot_power', 'attacking_finishing', 'attacking_volleys']
players2['shooting_avg2'] = players2[shooting_cols].mean(axis=1)
players2.drop(columns=shooting_cols, inplace=True)
players2.rename(columns={'shooting_avg2': 'shooting'}, inplace=True)

passing_cols = ['passing', 'attacking_crossing', 'attacking_short_passing', 'movement_reactions']
players2['passing_avg2'] = players2[passing_cols].mean(axis=1)
players2.drop(columns=passing_cols, inplace=True)
players2.rename(columns={'passing_avg2': 'passing'}, inplace=True)

players2.info()

y1 = players2['overall']
x1 = players2.drop('overall', axis=1)
x1

x1scaled = sc.fit_transform(x1)
x1 = pd.DataFrame(x1scaled, columns=x1.columns)
x1train,x1test,Y1train,Y1test=train_test_split(x1,y1,test_size=0.1,random_state=42)

rfg.fit(x1train, Y1train)
rfg_ypred2 =rfg.predict(x1test)
rfg_ypred2

rfgabsolute_err2 = mean_absolute_error(rfg_ypred2,Y1test)
rfgabsolute_err2

gbr.fit(x1train, Y1train)
gbr_ypred2 = gbr.predict(x1test)

gbrabsolute_err2 = mean_absolute_error(gbr_ypred2, Y1test)
gbrabsolute_err2

"""  Hyperparameter tuning"""

parameters_rfg = {
    'n_estimators': [10, 15, 20],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 6, 10]
}
parameters_gbr = {
    'n_estimators': [10, 15, 20],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.1, 0.01, 0.001]
}

rfg_gridsearch = GridSearchCV(estimator = RandomForestRegressor(), param_grid = parameters_rfg, scoring = 'neg_mean_absolute_error', cv=5)
rfg_gridsearch.fit(xtrain, Ytrain)
best_rfg = rfg_gridsearch.best_estimator_

gbr_gridsearch = GridSearchCV(estimator = GradientBoostingRegressor(), param_grid = parameters_gbr, scoring = 'neg_mean_absolute_error', cv=5)
gbr_gridsearch.fit(xtrain, Ytrain)
best_gbr = gbr_gridsearch.best_estimator_

bestrfg_ypred = best_rfg.predict(xtest)
best_rfg_abserr = mean_absolute_error(bestrfg_ypred, Ytest)
print("The mean absolute error for the best Random Forest Model is: ", best_rfg_abserr)

bestgbr_ypred = best_gbr.predict(xtest)
best_gbr_abserr = mean_absolute_error(bestgbr_ypred, Ytest)
print("The mean absolute error for the best Gradient Boost Regressor is: ", best_gbr_abserr)

ensemblemodel = VotingRegressor(estimators=[('rfg', rfg), ('gbr', gbr)])
ensemblemodel.fit(xtrain, Ytrain)
ensemblepredictions = ensemblemodel.predict(xtest)
print(ensemblepredictions)
print(xtest)
print(Ytest)

ensemble_abserr2 = mean_absolute_error(ensemblepredictions, Ytest)
ensemble_abserr2

"""Copying data to a file"""

scfile_path = '/content/drive/My Drive/players/scaler_ensemble.pkl'
joblib.dump(sc, scfile_path)

import pickle
spfile = '/content/drive/My Drive/Colab Notebooks/sports_prediction_ensemble_model.pkl'
pickle.dump(ensemblemodel, open(spfile, 'wb'))
loadedm = pickle.load(open(spfile, 'rb'))

