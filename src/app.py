# Third-party imports for web application
from dash import Dash, dcc, html, Input, Output, State, callback_context, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

# Related third party imports for data manipulation
import pandas as pd

# Local application/library specific imports
import validator as vd
import bpred as bp
import cpf
import visuals as vs
import os

# -------------------------------------------------------------------------------------------------------
# * program starts here

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Employee Retention Prediction Model"

app.layout = html.Div(
    children=[
        dcc.Store(id='kde_plot_selection_form_store'),
        dcc.Store(id='session_user_input'),
        html.Div(
            children=[
                html.P(children="📊", className="header-emoji"),
                html.H1(
                    children="Employee Retention Prediction Model",
                    className="header-title",
                ),
                html.P(
                    children=("A Machine Learning Approach using Random Forest Classifier"),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='Bar Charts', value='tab-1'),
            dcc.Tab(label='Heatmap', value='tab-2'),
            dcc.Tab(label='KDE Plot', value='tab-3'),
            dcc.Tab(label='Box Plot', value='tab-4'),
            dcc.Tab(label='AUROC Graph', value='tab-5'),
            dcc.Tab(label='Prediction Form', value='tab-6'),
        ]),
        html.Div(id='tabs-content')
    ]
)

# validator for the cpf inputs
@app.callback(
    [
     Output("satisfaction_level_cpf", "className"),
     Output("number_project_cpf", "className"),
     Output("average_monthly_hours_cpf", "className"),
     Output("time_spend_company_cpf", "className")
    ],
    [
     Input("satisfaction_level_cpf", "value"),
     Input("number_project_cpf", "value"),
     Input("average_monthly_hours_cpf", "value"),
     Input("time_spend_company_cpf", "value")
    ]
)
def update_classnames(satisfaction_level, number_project, average_monthly_hours, time_spend_company):
    return [
        "is-valid" if vd.validate_float(satisfaction_level) else "is-invalid",
        "is-valid" if vd.validate_integer(number_project) else "is-invalid",
        "is-valid" if vd.validate_amh_range(average_monthly_hours) else "is-invalid",
        "is-valid" if vd.validate_integer(time_spend_company) else "is-invalid"
    ]


# callback function that updates the value input at satisfaction level
# for example if user inputs .53 it turns into 0.53
# and if user insert 53 it will become 0.53
@app.callback(
    Output("satisfaction_level_cpf", "value"),
    [Input("satisfaction_level_cpf", "n_blur")],
    [State("satisfaction_level_cpf", "value")]
)
def update_satisfaction_level(n_blur, value):
    ctx = callback_context
    if not ctx.triggered:
        return no_update

    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id != 'satisfaction_level_cpf':
        return no_update
    if value is None:
        return no_update

    # Check for specific values
    if value == 100:
        return 1.00
    elif value == 1:
        return 0.01
    elif value > 1:
        return value / 100

    return no_update


# Callback function that updates the value of the disabled input field when the Submit button is clicked
# This callback function also is triggered by either the "submit_button_id" or the "save_button_id"
@app.callback(
    [
     # This output is used to display the prediction result
     Output("cpf_output", "value"),
     # This output is used to update the data in the DataTable
     Output("cpf_output_table", "data"),
     # This output is used to trigger the download of the DataFrame as a CSV file
     Output("download_dataframe_csv", "data"),
     # Session declaration so it doesn't override to_csv_inputs and table_csv_inputs
     Output('session_user_input', 'data')
    ],
    [
     # This input is the "Submit" button for making predictions
     Input("submit_button_id", "n_clicks"),
     # This input is the "Download" button for downloading the DataFrame as a CSV file
     Input("save_button_id", "n_clicks")
    ],
    [
     # These states are the inputs for making predictions
     State('satisfaction_level_cpf', 'value'),
     State('number_project_cpf', 'value'),
     State('average_monthly_hours_cpf', 'value'),
     State('time_spend_company_cpf', 'value'),
     State('salary_cpf', 'value'),
     State('department_cpf', 'value'),
     State('session_user_input', 'data')
    ]
)

def predict_or_save(n_clicks_submit, n_clicks_save, s_l, n_p, amh, tsc, sal, dep, session_data):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if session_data is None:
        session_data = {'to_csv_inputs': [], 'table_csv_inputs': []}
        
    # Check for specific values
    if isinstance(s_l, int) or isinstance(s_l, float):
        if s_l == 100:
            s_l = 1.00
        elif s_l == 1:
            s_l = 0.01
        elif s_l > 1:
            s_l = s_l / 100

    if button_id == "submit_button_id" and n_clicks_submit:
        # Check if any input is blank
        if not all([s_l, n_p, amh, tsc, sal, dep]):
            return "ERROR: Missing input or wrong input.", no_update, no_update, session_data

        # this one have 4 return values, so I arranged them this way and they have to be this way. see the last return part on bpred for reference.
        pred_output, pred_to_csv, sal_string, dep_string = bp.make_prediction(s_l, n_p, amh, tsc, sal, dep)
        # Store output for to csv / to save file
        session_data['to_csv_inputs'].append([s_l, n_p, amh, tsc, sal_string, dep_string, pred_output])
        # Store output for the table / used for displaying the user inputs in table
        session_data['table_csv_inputs'].append([s_l, n_p, amh, tsc, sal_string, dep_string, pred_to_csv])
        # Convert each list in cpf.table_csv_inputs to a dictionary that is going to be used in showing user inputs
        output_table_data = [dict(zip(cpf.table_csv_inputs_column_names, row)) for row in session_data['table_csv_inputs']]
        return pred_output, output_table_data, no_update, session_data

    elif button_id == "save_button_id" and n_clicks_save:
        df_output_table_data = pd.DataFrame(session_data['table_csv_inputs'], columns=cpf.table_csv_inputs_column_names)
        csv_string = df_output_table_data.to_csv(index=False, encoding='utf-8')
        # Clear the inputs list
        ses_to_csv = session_data['to_csv_inputs'] = []
        ses_table_csv = session_data['table_csv_inputs'] = []

        return ses_to_csv, ses_table_csv, dcc.send_string(csv_string, "saved_user_inputs.csv"), session_data

# needed for tab 3 to render the different plot types
@app.callback(
    Output('kde_plot_selection_form_store', 'data'),
    [Input('kde_plot_selection_form', 'value')]
)
def update_store(value):
    return value

#tabs
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value'),
     Input('kde_plot_selection_form_store', 'data')],
    [State('session_user_input', 'data')]
)
def render_content(tab, plot_type, session_data):
    if tab == 'tab-1':
        if session_data is not None:
            session_data['to_csv_inputs'] = []
            session_data['table_csv_inputs'] = []
        return dbc.Container([vs.bar_plot_selection_form])
    elif tab == 'tab-2':
        if session_data is not None:
            session_data['to_csv_inputs'] = []
            session_data['table_csv_inputs'] = []
        return dbc.Container([vs.corr_heatmap_container])
    elif tab == 'tab-3':
        if session_data is not None:
            session_data['to_csv_inputs'] = []
            session_data['table_csv_inputs'] = []
        return dbc.Container([
            vs.kde_plot_selection_form,
            html.Hr(),
            vs.kde_static_plot if plot_type == 'static_plot' else vs.kde_interactive_plot if plot_type == 'interactable_plot' else dbc.Alert('Error: Invalid plot type selected', color='danger')
        ])
    elif tab == 'tab-4':
        if session_data is not None:
            session_data['to_csv_inputs'] = []
            session_data['table_csv_inputs'] = []
        return dbc.Container([vs.box_plot_container])
    elif tab == 'tab-5':
        if session_data is not None:
            session_data['to_csv_inputs'] = []
            session_data['table_csv_inputs'] = []
        return dbc.Container([vs.auroc_container])
    elif tab == 'tab-6':
        return dbc.Container([
            html.Hr(),
            html.H3("Custom Prediction Input Form"),
            cpf.custom_prediction_form
        ])


# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=False)