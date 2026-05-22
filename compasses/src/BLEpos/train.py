#imports
from BLEpos.data_collectors import rssiCoordCollector
from BLEpos.model_trainers import randomForestTrainerAggregated

print("Collecting RSSI data and training a Random Forest on it")

# get arguments for data collector
filename = str(input('enter id for space: '))
n = int(input('enter number of scans: '))

rssiCoordCollector.collect(filename,n) # run data collector

print('data collection finished!')
print('now lets train the model...')

randomForestTrainerAggregated.train(filename,10) # run model trainer on collected data
