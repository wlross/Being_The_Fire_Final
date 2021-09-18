import numpy as np
import os
import tensorflow
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, Flatten
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from datetime import datetime

os.chdir("/Users/wlross/Desktop/Capstone/Working/BulkData")
newX = np.load('lastXData_1775535.npy')
finalX = newX[:-1]
print(finalX.shape)
newY = np.load('lastYData_1775535.npy')
finalY = newY[:-1]
print(finalY.shape)

# Shuffle and split random train and test set
#X_train, X_test, y_train, y_test = train_test_split(finalX, finalY, test_size=.2, random_state=42, shuffle=True)
X_train, X_test, y_train, y_test = train_test_split(finalX, finalY, test_size=.2, random_state=42, shuffle=True, stratify = finalY)
print(X_train.shape)
print(y_train.shape)

# Clear memory to train new network and set learning rate and class eights
tensorflow.keras.backend.clear_session()
dasLearnRate = .00001 #was .00001
class_weights = {0: 1, 1: 4} #was 4


# Define neural network architecture and compile the model
burnModel = Sequential()
burnModel.add(Conv2D(32, (2, 2), activation='relu', input_shape=(11, 3, 3)))
burnModel.add(Conv2D(64, (2, 2), activation='relu'))
burnModel.add(Flatten())
burnModel.add(Dense(64, activation='relu'))
burnModel.add(Dropout(0.4))
burnModel.add(Dense(128, activation='relu'))
burnModel.add(Dropout(0.2))
burnModel.add(Dense(64, activation='relu'))
burnModel.add(Dense(32, activation='relu'))
burnModel.add(Dense(1, activation='sigmoid'))
burnModel.summary()
opt = keras.optimizers.Adam(learning_rate=dasLearnRate)

burnModel.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])


# Train Model
history = burnModel.fit(X_train, y_train, class_weight=class_weights, epochs=300) #was 3

# get unique id for file/model saving
current_datetime = datetime.now()
day = str(int(current_datetime.day))
hour = str(int(current_datetime.hour))
minute = str(int(current_datetime.minute))
second = str(int(current_datetime.second))
uId = day + hour + minute + second

# SAVE model..
os.chdir("/Users/wlross/Desktop/Capstone/Working/Working/spring_model")
saveModelName = 'currentmodel' + uId + '.h5'
burnModel.save(saveModelName)

# Make Predictions
y_pred = burnModel.predict_classes(X_test)

print(classification_report(y_test, y_pred))
