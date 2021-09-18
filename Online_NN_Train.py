import os
import time
import warnings
from datetime import datetime
import random
import pandas as pd
import numpy as np
import tensorflow
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, Flatten
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def get_neighbors(index, data):
    thisLeft = data.loc[index, 'left']
    thisTop = data.loc[index, 'top']
    thisRight = data.loc[index, 'right']
    thisBottom = data.loc[index, 'bottom']

    upCell = data[data['top'] == thisBottom]
    upCell = upCell[upCell['left'] == thisLeft]
    if upCell.empty:
        upCell = None
    else:
        upCell = upCell['id'].iloc[0]

    downCell = data[data['bottom'] == thisTop]
    downCell = downCell[downCell['right'] == thisRight]
    if downCell.empty:
        downCell = None
    else:
        downCell = downCell['id'].iloc[0]

    leftCell = data[data['left'] == thisRight]
    leftCell = leftCell[leftCell['top'] == thisTop]
    if leftCell.empty:
        leftCell = None
    else:
        leftCell = leftCell['id'].iloc[0]

    rightCell = data[data['right'] == thisLeft]
    rightCell = rightCell[rightCell['bottom'] == thisBottom]
    if rightCell.empty:
        rightCell = None
    else:
        rightCell = rightCell['id'].iloc[0]

    return (upCell, downCell, leftCell, rightCell)


def noNan(ini_array):
    # find indices where nan value is present
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        col_mean = np.nanmean(ini_array, axis=0)
    inds = np.where(np.isnan(ini_array))
    ini_array[inds] = np.take(col_mean, inds[1])
    newArr = ini_array
    return newArr


def getMatrix(neighbor, data):
    upNe, downNe, leftNe, rightNe = get_neighbors(neighbor,
                                                  data)  # given neighbor as center, get up, down, left and right
    upUp, downUp, leftUp, rightUp = get_neighbors(upNe, data)  # get left and right of up for corners
    upDown, downDown, leftDown, rightDown = get_neighbors(downNe, data)  # get left and right of down for corners
    strHead = 'Red_mean'
    Red = np.array([[data.loc[leftUp, strHead], data.loc[upNe, strHead], data.loc[rightUp, strHead]],
                    [data.loc[leftNe, strHead], data.loc[neighbor, strHead], data.loc[rightNe, strHead]],
                    [data.loc[leftDown, strHead], data.loc[downNe, strHead], data.loc[rightDown, strHead]]],
                   dtype=np.float32)
    strHead = 'Green_mean'
    Green = np.array([[data.loc[leftUp, strHead], data.loc[upNe, strHead], data.loc[rightUp, strHead]],
                      [data.loc[leftNe, strHead], data.loc[neighbor, strHead], data.loc[rightNe, strHead]],
                      [data.loc[leftDown, strHead], data.loc[downNe, strHead], data.loc[rightDown, strHead]]],
                     dtype=np.float32)
    strHead = 'Blue_mean'
    Blue = np.array([[data.loc[leftUp, strHead], data.loc[upNe, strHead], data.loc[rightUp, strHead]],
                     [data.loc[leftNe, strHead], data.loc[neighbor, strHead], data.loc[rightNe, strHead]],
                     [data.loc[leftDown, strHead], data.loc[downNe, strHead], data.loc[rightDown, strHead]]],
                    dtype=np.float32)
    strHead = 'REdge_mean'
    RedEdge = np.array([[data.loc[leftUp, strHead], data.loc[upNe, strHead], data.loc[rightUp, strHead]],
                        [data.loc[leftNe, strHead], data.loc[neighbor, strHead], data.loc[rightNe, strHead]],
                        [data.loc[leftDown, strHead], data.loc[downNe, strHead], data.loc[rightDown, strHead]]],
                       dtype=np.float32)
    strHead = 'NIR_mean'
    NearIR = np.array([[data.loc[leftUp, strHead], data.loc[upNe, strHead], data.loc[rightUp, strHead]],
                       [data.loc[leftNe, strHead], data.loc[neighbor, strHead], data.loc[rightNe, strHead]],
                       [data.loc[leftDown, strHead], data.loc[downNe, strHead], data.loc[rightDown, strHead]]],
                      dtype=np.float32)
    strHead = 'Z_mean'
    Elev = np.array([[data.loc[leftUp, strHead], data.loc[upNe, strHead], data.loc[rightUp, strHead]],
                     [data.loc[leftNe, strHead], data.loc[neighbor, strHead], data.loc[rightNe, strHead]],
                     [data.loc[leftDown, strHead], data.loc[downNe, strHead], data.loc[rightDown, strHead]]],
                    dtype=np.float32)
    strHead = 'MAX_speed'
    WindMaxSpd = np.array([[data.loc[leftUp, strHead], data.loc[upNe, strHead], data.loc[rightUp, strHead]],
                           [data.loc[leftNe, strHead], data.loc[neighbor, strHead], data.loc[rightNe, strHead]],
                           [data.loc[leftDown, strHead], data.loc[downNe, strHead], data.loc[rightDown, strHead]]],
                          dtype=np.float32)
    strHead = 'MAX_dir'
    WindMaxDir = np.array([[data.loc[leftUp, strHead], data.loc[upNe, strHead], data.loc[rightUp, strHead]],
                           [data.loc[leftNe, strHead], data.loc[neighbor, strHead], data.loc[rightNe, strHead]],
                           [data.loc[leftDown, strHead], data.loc[downNe, strHead], data.loc[rightDown, strHead]]],
                          dtype=np.float32)
    strHead = 'AVG_speed'
    WindAvgSpeed = np.array([[data.loc[leftUp, strHead], data.loc[upNe, strHead], data.loc[rightUp, strHead]],
                             [data.loc[leftNe, strHead], data.loc[neighbor, strHead], data.loc[rightNe, strHead]],
                             [data.loc[leftDown, strHead], data.loc[downNe, strHead], data.loc[rightDown, strHead]]],
                            dtype=np.float32)
    strHead = 'AVG_dir'
    WindAvgDir = np.array([[data.loc[leftUp, strHead], data.loc[upNe, strHead], data.loc[rightUp, strHead]],
                           [data.loc[leftNe, strHead], data.loc[neighbor, strHead], data.loc[rightNe, strHead]],
                           [data.loc[leftDown, strHead], data.loc[downNe, strHead], data.loc[rightDown, strHead]]],
                          dtype=np.float32)
    strHead = 'currFire'
    currFire = np.array([[data.loc[leftUp, strHead], data.loc[upNe, strHead], data.loc[rightUp, strHead]],
                         [data.loc[leftNe, strHead], data.loc[neighbor, strHead], data.loc[rightNe, strHead]],
                         [data.loc[leftDown, strHead], data.loc[downNe, strHead], data.loc[rightDown, strHead]]],
                        dtype=np.float32)
    mylist = [Red, Green, Blue, RedEdge, NearIR, Elev, WindMaxSpd, WindMaxDir, WindAvgSpeed,
              WindAvgDir, currFire]
    for lyr in mylist:
        lyr = noNan(lyr)
    new = np.stack(mylist)
    new = noNan(new)
    # print(new.shape)
    # print(new)
    return new


# Define fire train vs. test datasets
allFire = ['BUCK', 'COVE', 'CREEK', 'Cub Creek',
           'Gutzler', 'HELENA', 'Highline', 'Indian Ridge',
           'Little Hogback', 'Mammoth Cave', 'NENA SPRINGS',
           'North Pelican', 'OAK', 'Pinal', 'Powerline', 'Preacher',
           'SADDLE', 'SHEEP', 'STEELE', 'Sulfur', 'SWISSHELMS']
testFire = ['Buck', 'Highline', 'Pinal', 'Sulfur']
trainFire = ['COVE', 'CREEK', 'Cub Creek',
             'Gutzler', 'HELENA', 'Indian Ridge',
             'Little Hogback', 'Mammoth Cave', 'NENA SPRINGS',
             'North Pelican', 'OAK', 'Powerline', 'Preacher',
             'SADDLE', 'SHEEP', 'STEELE', 'SWISSHELMS']

# hyperparameters
speedParam = 1.7
traindim = 1000

# Clear memory to train new network
tensorflow.keras.backend.clear_session()

# Import existing Neural network architecture and print summary of model architecture
os.chdir("/Users/wlross/Desktop/Capstone/Working/Working/spring_online_models")
burnModel = keras.models.load_model('0911_150_EvalModel_6231122.h5')
burnModel.summary()

for thisFire in testFire:
    print(thisFire)
    print("do a test run!")
    os.chdir("/Users/wlross/Desktop/Capstone/Working/Working/csv_files")
    currDir = os.getcwd()
    os.chdir(currDir + "/" + thisFire)
    data = pd.read_csv(thisFire + ".csv")
    tik = time.time()
    onFire = data[data['currFire'] == 1]
    fireSpeed = int(round(speedParam * data.loc[0, 'MAX_speed']))
    for j in range(0, fireSpeed):
        tik=time.time()
        print('New Iteration')
        print(j)
        print(fireSpeed)
        for index, row in onFire.iterrows():
            #print("yay")
            up, down, left, right = get_neighbors(index, data)
            neighbors = [up, down, left, right]
            # print(neighbors)
            for neighbor in neighbors:
                if neighbor == None:  # ... if the neighbor is an edge... skip it
                    continue
                if data.loc[neighbor, 'zero_incid'] == thisFire:  # ... if the neighbor already burned skip it...
                    continue
                if data.loc[neighbor, 'currFire'] == thisFire:  # ... if the neighbor already burned skip it...
                    continue
                else:
                    # print("go-time")
                    try:
                        matrix = getMatrix(neighbor, data)
                    except:
                        continue

                    preMat = np.zeros((traindim, 11, 3, 3))
                    preMat[0] = matrix
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        predLive = burnModel.predict_classes(preMat)
                    predLive = int(predLive[0])
                    data.loc[neighbor, 'currFire'] = predLive
        tok=time.time()
        print("Iteration took:")
        print(tok-tik)
    # get unique id for file/model saving
    current_datetime = datetime.now()
    day = str(int(current_datetime.day))
    hour = str(int(current_datetime.hour))
    minute = str(int(current_datetime.minute))
    second = str(int(current_datetime.second))
    uId = day + hour + minute + second

    # SAVE data as a complete fire test....
    os.chdir("/Users/wlross/Desktop/Capstone/Working/Working/test_results")
    saveFileName = thisFire + '_latest_test_' + uId + '.csv'
    data.to_csv(saveFileName)






