# Standard library imports
import os

# Related third party imports for data manipulation
import pandas as pd

# Related third party imports for machine learning
from sklearn.model_selection import train_test_split

# Related third party imports for model persistence
import joblib

# * UNIVERSAL VARIABLE

universal_features = [
    'Age_group_Young_Adults', 'Age_group_Adults',
    'EnvironmentSatisfaction', 'JobInvolvement', 'JobLevel',
    'JobSatisfaction', 'MonthlyIncome', 'OverTime_Yes',
    'PerformanceRating', 'RelationshipSatisfaction', 'TotalWorkingYears',
    'WorkLifeBalance', 'YearsAtCompany', 'YearsSinceLastPromotion'
  ]

universal_target = 'Attrition_Yes'

universal_all_variable = [
    'Age_group_Young_Adults', 'Age_group_Adults',
    'EnvironmentSatisfaction', 'JobInvolvement', 'JobLevel',
    'JobSatisfaction', 'MonthlyIncome', 'OverTime_Yes',
    'PerformanceRating', 'RelationshipSatisfaction', 'TotalWorkingYears',
    'WorkLifeBalance', 'YearsAtCompany', 'YearsSinceLastPromotion', 'Attrition_Yes'
  ]

# -------------------------------------------------------------------------------------------------------
# * for model accuracy test
# Implementing Random Forest model
df_bpred = pd.read_csv('https://raw.githubusercontent.com/CS-DREAM-TEAM/assets/main/ibm_hr_acc_test.csv')

# Initializing inputs and targets
bpred_inputs = df_bpred[universal_features]
bpred_target = df_bpred[universal_target]

# Implementing the ML Train Test Split Method
x_train, x_test, y_train, y_test = train_test_split(bpred_inputs, bpred_target, train_size=0.8)

# -------------------------------------------------------------------------------------------------------
# * the model itself

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the file using a relative path
file_path = os.path.join(script_dir, 'rf_model_4.0.5_NOPARAM.joblib')

# Load the file using the constructed path
loaded_rf_model = joblib.load(file_path)


age_mapping = {
    'a_gro_ya'      : [1,0],
    'a_gro_a'       : [0,1],
    'a_gro_ret'     : [0,0]
}

def make_prediction(env_s, j_stf, r_sts, pf_rt, wl_bl, j_inv, j_lvl, a_gro, ovr_t, m_inc, y_com, tw_yr, y_prm):
    # ************************************
    # * These are used in the cpf_output_table

    # Convert Generation Group code to full name
    orig_name_gg_mapping = {'a_gro_ya'      : 'Young Adult (18-30)',
                            'a_gro_a'       : 'Adult (30-60)',
                            'a_gro_ret'     : 'Near Retirement (60+)' }
    gen_g_string = orig_name_gg_mapping[a_gro]

    # ************************************

    columns = universal_features

    # Department_mapping
    age_type = age_mapping.get(a_gro)
    
    # Initialization of dataframe with the custom prediction data
    prediction_data = pd.DataFrame([age_type + [env_s, j_inv, j_lvl, j_stf, m_inc, ovr_t, pf_rt, r_sts, tw_yr, wl_bl, y_com, y_prm]], columns = columns)
    # Predict
    model_score = float(loaded_rf_model.score(x_test,y_test))
    pred_data = loaded_rf_model.predict(prediction_data)
    pred_output = ''
    pred_to_csv = ''

    if pred_data == [0]:
        pred_output = ('Employee predicted to STAY.' + ' Confidence: ' + ('{:.2%}'.format(model_score)))
        pred_to_csv = ('STAY')
    else:
        pred_output = ('Employee predicted to LEAVE.' + ' Confidence: ' + ('{:.2%}'.format(model_score)))
        pred_to_csv = ('LEAVE')

    return pred_output, pred_to_csv, gen_g_string