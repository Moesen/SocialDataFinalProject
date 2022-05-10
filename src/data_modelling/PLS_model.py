import argparse
import os
import pdb

import numpy as np
import pandas as pd
import warnings
from sklearn.preprocessing import scale 
from sklearn import model_selection
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import train_test_split
from sklearn.cross_decomposition import PLSRegression

import pickle

def is_dir(path: str) -> str:
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)


def train_model_and_save_loadings(in_path: str, out_path: str):
    df_social_sub = pd.read_csv(in_path + "/ml_processed_data.csv", index_col=0)
    
    # Define target values and features
    X = df_social_sub.iloc[:,:-1]
    y = df_social_sub.iloc[:,-1]

    # Select data 
    Continent = 'all'
    year_max = 2019
    year_min = 2000

    X1 = X.copy()
    y1 = y.copy()

    if Continent == 'all':
        X1 = X1[(X['Year'] <= year_max) & (X['Year'] >= year_min)]
        y1 = y1[(X['Year'] <= year_max) & (X['Year'] >= year_min)]

        X1 = pd.concat([X1,pd.get_dummies(X1.Continent, prefix='Continent')],axis=1)
    else:
        X1 = X1[(X['Year'] <= year_max) & (X['Year'] >= year_min) & (X['Continent'] == Continent)]
        y1 = y1[(X['Year'] <= year_max) & (X['Year'] >= year_min) & (X['Continent'] == Continent)]

    X1 = X1.reset_index().drop(columns='index')
    y1 = y1.reset_index().drop(columns='index')

    # Drop years and continent from features dataset
    X2 = X1.iloc[:,3:]

    # Get training and test set
    X_train,X_test,y_train,y_test = train_test_split(X2,y1,test_size=0.3,random_state=0) 

    #define cross-validation method
    cv = RepeatedKFold(n_splits=20, n_repeats=3, random_state=1)

    mse = []
    n = X_train.shape[1]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore") #Ignore runtime warning (divide by zero)

        # Calculate MSE using cross-validation, adding one component at a time
        for i in np.arange(1, n):
            pls = PLSRegression(n_components=i)
            score = -1*model_selection.cross_val_score(pls, scale(X_train), y_train, cv=cv,
                    scoring='neg_mean_squared_error').mean()
            mse.append(score)


    #calculate RMSE
    pls = PLSRegression(n_components=np.argmin(mse)+1)
    X_mean = X_train.mean()
    X_std = X_train.std()
    pls.fit(scale(X_train), y_train)
    
    # Get fitted values
    X_test_std = (X_test-X_mean)/X_std
    y_test_dat = y_test.to_numpy().ravel()
    y_hat_dat = pls.predict(X_test_std.to_numpy()).ravel()

    # Get test_data and predictions
    sort_indx = np.argsort(y_hat_dat)
    y_test_sorted = y_test_dat[sort_indx]
    y_hat_sorted = y_hat_dat[sort_indx]

    test_data = pd.DataFrame({'y_test':y_test_sorted,'y_hat':y_hat_sorted, 'y_cont':X1['Continent'].iloc[X_test.index]})

    # Extract loadings 
    n_comp = 3

    with warnings.catch_warnings():
        warnings.simplefilter("ignore") #Ignore runtime warning (divide by zero)
        loadings=pd.DataFrame(pls.x_loadings_.T)
        loadings.columns = X2.columns

        loadings_v = loadings.unstack().reset_index()
        loadings_v.columns = ['Feature','PLS Component','Loading']

        loadings_v = loadings_v[loadings_v['PLS Component'] < n_comp]
        loadings_v['Continent'] = np.array(['Continent' in x for x in loadings_v['Feature']])
        loadings_v['x'] = np.array([0,0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,
                                    1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6])
        loadings_v['PLS Component'] = loadings_v['PLS Component']+1

        loadings_v_social = loadings_v.iloc[['Continent' not in x for x in loadings_v['Feature']],:]
        loadings_v_continent = loadings_v.iloc[['Continent' in x for x in loadings_v['Feature']],:]
        loadings_v_continent.rename(columns={'Feature':'Continent'},inplace=True)
        #loadings_v_continent.loc[:,'Continent'] = np.array([x.split('_')[1] for x in loadings_v_continent['Continent']])

    social_feats = pd.Series([x for x in loadings_v['Feature'] if 'Continent' not in x]).unique()
    continents = pd.Series([x for x in loadings_v['Feature'] if 'Continent' in x]).unique()
    continents = np.array([x.split('_')[1] for x in continents])
    loadings_v = loadings_v.reset_index().drop(columns='index')

    for indx,feat in enumerate(loadings_v['Feature']):
        if "Continent" in feat:
            loadings_v.loc[indx,'Feature'] = feat.split('_')[1]

    # Save data
    test_data.to_csv(os.path.join(out_path, f"test_data.csv"))
    loadings_v.to_csv(os.path.join(out_path, f"loadings_v.csv"))
    y_loadings = pd.Series(pls.y_loadings_.ravel())
    y_loadings.to_csv(os.path.join(out_path, f"y_loadings_v.csv"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess ml data")
    parser.add_argument("--in_path", type=is_dir)
    parser.add_argument("--out_path", type=is_dir)
    args = parser.parse_args()

    in_path, out_path = args.in_path, args.out_path
    train_model_and_save_loadings(in_path, out_path)
