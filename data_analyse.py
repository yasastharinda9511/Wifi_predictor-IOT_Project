import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import os
from sklearn.metrics import classification_report, confusion_matrix


wifi_data = pd.read_csv("wifi_data.csv")
unknowndata = pd.read_csv("unknown_data.csv")
filename="predictionFile"
#print("Dimensions of the data:")
#print(wifi_data.shape)
#print("\nFirst few records:")
#print(wifi_data.head())

X = wifi_data.drop('id', axis=1)  #contains attributes
y = wifi_data['id']

ssid_train, ssid_test, id_train, id_test = train_test_split(X, y, test_size = 0.6)
print(len(ssid_test),len(id_test))

svclassifier = SVC(kernel='linear')
svclassifier.fit(ssid_train, id_train)
prediction=np.array([-100.0,-61.0,-100.0,-100.0,-62.0,-100.0,-79.0,-66.0,-100.0])
prediction=prediction.reshape(1,-1)
id_pred = svclassifier.predict(ssid_test)
l=svclassifier.predict(unknowndata)
print(l)
def write_to_csv():
    global unknowndata
    global filename,l
    count = 0
    unknowndata=unknowndata.values
    print(unknowndata)
    result = {"UoM_Wireless1": -100, "UoM_Wireless6": -100, "UoM_Wireless11": -100, "eduroam1": -100, "eduroam6": -100,
              "eduroam11": -100, "Jungle Book10": -100, "PROLINK_H5004NK_8766E11": -100}
    z=list(result.keys())
    for i in range(len(unknowndata)):
        print(unknowndata[i])
        for r in range (len(z)):
            result[z[r]]=unknowndata[i][r]
        result["id"]=l[i]
        df = pd.Series(result).to_frame().T
        df.to_csv(filename, index=False, mode='a', header=(not os.path.exists(filename)))
        count = 0
print(id_pred)
write_to_csv()
