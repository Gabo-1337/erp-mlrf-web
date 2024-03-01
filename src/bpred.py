import os

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

# -------------------------------------------------------------------------------------------------------
# * for model accuracy test
# Implementing Random Forest model
df = pd.read_csv('https://raw.githubusercontent.com/CS-DREAM-TEAM/assets/main/HR_comma_sep.csv')

# Dropping all duplicate data
df.drop_duplicates(inplace = True)

# Initializing inputs and targets
inputs = df[['satisfaction_level','number_project','average_montly_hours','time_spend_company','Department','salary']]
target = df.left

# Setting all salary values in numerical values
inputs.replace({'salary': {'low':1, 'medium':2, 'high':3}}, inplace=True)

# One Hot Encoding implementation
dep_dummies = pd.get_dummies(df['Department'])
df_with_dummies = pd.concat([inputs,dep_dummies],axis='columns')
df_with_dummies.drop('Department',axis='columns',inplace=True)
df_with_dummies.drop('technical',axis='columns',inplace=True)

# Implementing x and y for prediction model
x = df_with_dummies
y = target

# Implementing the ML Train Test Split Method
x_train, x_test, y_train, y_test = train_test_split(x,y,train_size=0.8)

# -------------------------------------------------------------------------------------------------------
# * the model itself

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the file using a relative path
file_path = os.path.join(script_dir, 'employee_model.joblib')

# Load the file using the constructed path
model = joblib.load(file_path)

department_mapping = {
    "IT":          [1,0,0,0,0,0,0,0,0],
    "RandD":       [0,1,0,0,0,0,0,0,0],
    "accounting":  [0,0,1,0,0,0,0,0,0],
    "hr":          [0,0,0,1,0,0,0,0,0],
    "management":  [0,0,0,0,1,0,0,0,0],
    "marketing":   [0,0,0,0,0,1,0,0,0],
    "product_mng": [0,0,0,0,0,0,1,0,0],
    "sales":       [0,0,0,0,0,0,0,1,0],
    "support":     [0,0,0,0,0,0,0,0,1],
    "technical":   [0,0,0,0,0,0,0,0,0]
}

def make_prediction(s_l, n_p, amh, tsc, sal, dep):
    # Department_mapping
    d_type = department_mapping.get(dep)
    # Defining the columns
    columns = ['satisfaction_level','number_project','average_montly_hours','time_spend_company','salary','IT','RandD','accounting','hr','management','marketing','product_mng','sales','support']

    # Initialization of dataframe with the custom prediction data
    prediction_data = pd.DataFrame([[s_l, n_p, amh, tsc, sal] + d_type], columns=columns)

    # Predict
    model_score = float(model.score(x_test,y_test))
    pred_data = model.predict(prediction_data)
    pred_output = "No output yet"
    if pred_data == [0]:
        # * removed "(value returned was " + str(pred_data) + ")" +
        pred_output = ("The employee is highly likely to STAY in the company. " + " Confidence: " + ("{:.2%}".format(model_score)))
    else:
        pred_output = ("The employee is highly likely to LEAVE the company. " + " Confidence: " + ("{:.2%}".format(model_score)))
  
    return pred_output