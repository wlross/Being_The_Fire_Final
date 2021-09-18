import numpy as np
import os
import math
from sklearn.metrics import classification_report


import pandas as pd

#TODO: Update each fire
os.chdir("/Users/wlross/Desktop/Capstone/Working/Working/test_results")
data = pd.read_csv("Buck_Farsite_Test.csv")
fireName = "BUCK"

yPred = []
yTrue = []

for index, row in data.iterrows():
    thisPred = data.loc[index, 'Farsite_Pred'] #TODO:Toggle currFire or Farsite_Pred
    thisTrue = data.loc[index, 'one_incide']
    thisAlrd = data.loc[index, 'zero_incid']
    if thisAlrd == fireName:
        continue
    elif thisTrue == fireName and math.isnan(thisPred):
        myVal = 0
        yPred.append(myVal)
        myVal = 1
        yTrue.append(myVal)
    elif math.isnan(thisPred) and math.isnan(thisPred):
        myVal = 0
        yPred.append(myVal)
        yTrue.append(myVal)
    elif math.isnan(thisPred):
        continue
    else:
        yPred.append(thisPred)
        if thisTrue == fireName:
            myVal = 1
            yTrue.append(myVal)
        else:
            myVal = 0
            yTrue.append(myVal)

print(yPred)
print(len(yPred))
print(yTrue)
print(len(yTrue))

print(classification_report(yTrue, yPred))



