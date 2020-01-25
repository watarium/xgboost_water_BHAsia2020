import pandas as pd
import xgboost as xgb
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
import pickle

df = pd.read_csv('water_supply_retraining.csv')
X_train_validate, X_test, y_train_validate, y_test = train_test_split(df.drop('water', axis=1), df['water'].ravel())

grid_best_params = joblib.load('grid_best_params.pkl')
regressor = joblib.load('water_supply.pkl')

# Fit by best params
regressor = xgb.XGBRegressor(learning_rate=grid_best_params['learning_rate'],
                             max_depth=grid_best_params['max_depth'],
                             n_estimators=grid_best_params['n_estimators'])
regressor.fit(X_train_validate, y_train_validate, verbose=False)

# Save model
#pickle.dump(grid_best_params, open('grid_best_params.pkl', 'wb'))
pickle.dump(regressor, open('water_supply.pkl', 'wb'))

# Prediction
for hour in range(1,24):
    for temperature in range(5,40):
        input = pd.DataFrame([[hour, temperature]], columns=['hour', 'temperature'])
        result = regressor.predict(input)
        print('Hour: ' + str(hour) + '  Temperature: ' + str(temperature) + '  Prediction: ' + str(result[0]))