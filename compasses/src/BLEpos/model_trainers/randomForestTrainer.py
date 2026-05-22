# import modules
print("importing modules for training...")
import sklearn
assert sklearn.__version__ >= "1.0"
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import joblib
import pandas as pd
from importlib import resources as impresources
import BLEpos.data as dataDir
import BLEpos.models as modelsDir

# train Random Forest model function passing filename for RSSI data and number of estimators or decision trees in the forest
def train(filename, n_est):

    file = impresources.files(dataDir) / f"{filename}.csv"
    
    # load data
    print("loading data...")
    data = pd.read_csv(file)
    print("data loaded")
    
    #parse data into features (RSSI values for each beacon) and targets (coordinates)
    features = data.drop(columns=['x','y'])
    targets = data[['x','y']]

    # combine x and y coordinate so we are just training a single random forest classifier
    target_coord = data['x'].astype(str) + ',' + data['y'].astype(str)
    
    # split the data into train and test sets
    features_train, features_test, targets_train, targets_test = train_test_split(features, target_coord, test_size=0.2, random_state=29)

    # initiate Random Forest model with the given number of estimators
    print("training Random Forest...")
    rf = RandomForestClassifier(n_estimators=n_est, random_state=29, n_jobs=-1)
    rf.fit(features_train, targets_train) # train the model using the train data set
    print("model trained!")

    targets_predict = rf.predict(features_test) # predict the coordinates for the test rssi data

    accuracy = accuracy_score(targets_test, targets_predict) # find the accuracy of this prediction
    print(f"Accuracy: {accuracy:.4f}")
    
    # print some of the prediction results to visualise
    results = pd.DataFrame({
        'Actual Coord': targets_test,
        'Pred. Coord': targets_predict
    })
    
    print("First few predictions:")
    print(results.head())
    
    model_file = impresources.files(modelsDir) / f"{filename}.joblib"
    joblib.dump(rf, model_file)

    print(f"model saved to models/{filename}.joblib!")
    
# if this file is run as a standalone script
if __name__ == "__main__":

    print("Random Forest Classification Trainer!")
    filename = str(input("enter data filename: "))
    n = int(input("enter number of estimators or decision trees for the model: "))

    trainModel(filename, n)
