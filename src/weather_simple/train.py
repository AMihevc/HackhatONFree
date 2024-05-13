import pandas as pd

# start training a model
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import xgboost as xgb

DATA_OUT_TRAIN_X = "/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/data_out/koroska_macro_train_X.pkl"
DATA_OUT_TRAIN_Y = "/d/hpc/home/tp1859/HackhatONFree/src/weather_simple/data_out/koroska_macro_train_y.pkl"


df_X = pd.read_pickle(DATA_OUT_TRAIN_X)
df_y = pd.read_pickle(DATA_OUT_TRAIN_Y)

print(df_X.head())
print(df_y.head())


X_train, X_val, y_train, y_val = train_test_split(df_X, df_y, test_size=0.2, random_state=42)


print("Training Random Forest")
model_rf = RandomForestClassifier(n_estimators=3000, random_state=42)
model_rf.fit(X_train, y_train)
y_pred_rf = model_rf.predict(X_val)

print("Accuracy Random Forest: ", accuracy_score(y_val, y_pred_rf))
print(classification_report(y_val, y_pred_rf))



# model_adaboost = AdaBoostClassifier(n_estimators=300, random_state=42)
# model_adaboost.fit(X_train, y_train)


# TODO: xgboost
model = xgb.XGBClassifier(objective="multi:softmax", num_class=3, n_estimators=3000, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_val)

print("Accuracy XGBoost: ", accuracy_score(y_val, y_pred))
print(classification_report(y_val, y_pred))


