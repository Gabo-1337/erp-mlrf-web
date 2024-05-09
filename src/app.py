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


# -------------------------------------------------------------------------------------------------------
# * program starts here

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Employee Retention Prediction Model"
server = app.server

app.layout = html.Div(
    children=[
        dcc.Store(id='kde_plot_selection_form_store'),
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
# This callback function also is triggered by either the "submit-button-id" or the "save-button-id"
@app.callback(
    [
     # This output is used to display the prediction result
     Output("cpf_output", "value"),
     # This output is used to update the data in the DataTable
     Output("cpf_output_table", "data"),
     # This output is used to trigger the download of the DataFrame as a CSV file
     Output("download-dataframe-csv", "data")
    ],
    [
     # This input is the "Submit" button for making predictions
     Input("submit-button-id", "n_clicks"),
     # This input is the "Download" button for downloading the DataFrame as a CSV file
     Input("save-button-id", "n_clicks")
    ],
    [
     # These states are the inputs for making predictions
     State('satisfaction_level_cpf', 'value'),
     State('number_project_cpf', 'value'),
     State('average_monthly_hours_cpf', 'value'),
     State('time_spend_company_cpf', 'value'),
     State('salary_cpf', 'value'),
     State('department_cpf', 'value')
    ]
)

def predict_or_save(n_clicks_submit, n_clicks_save, s_l, n_p, amh, tsc, sal, dep):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "submit-button-id":
        if n_clicks_submit:
            # Check if any input is blank
            if not all([s_l, n_p, amh, tsc, sal, dep]):
                return "ERROR: Missing input or wrong input.", no_update, no_update
            else:
                # this one have 2 return values, so I arranged them this way, see the last return part on bpred for reference.
                pred_output, pred_to_csv = bp.make_prediction(s_l, n_p, amh, tsc, sal, dep)
                # Store output for to csv / to save file
                cpf.to_csv_inputs.append([s_l, n_p, amh, tsc, sal, dep, pred_output])
                # Store output for the table / used for displaying the user inputs in table
                cpf.table_csv_inputs.append([s_l, n_p, amh, tsc, sal, dep, pred_to_csv])
                # Convert each list in cpf.table_csv_inputs to a dictionary that is going to be used in showing user inputs
                output_table_data = [dict(zip(cpf.table_csv_inputs_column_names, row)) for row in cpf.table_csv_inputs]
                return pred_output, output_table_data, no_update

    elif button_id == "save-button-id":
        if n_clicks_save:
            df_output_table_data = pd.DataFrame(cpf.table_csv_inputs, columns=cpf.table_csv_inputs_column_names)
            csv_string = df_output_table_data.to_csv(index=False, encoding='utf-8')
            # Clear the inputs list
            cpf.to_csv_inputs = []
            cpf.table_csv_inputs = []

            return cpf.to_csv_inputs, cpf.table_csv_inputs, dcc.send_string(csv_string, "saved_user_inputs.csv")


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
     Input('kde_plot_selection_form_store', 'data')]
)
def render_content(tab, plot_type):
    if tab == 'tab-1':
        cpf.to_csv_inputs = []
        cpf.table_csv_inputs = []
        return dbc.Container([vs.bar_chart_container])
    elif tab == 'tab-2':
        return dbc.Container([vs.corr_heatmap_container])
    elif tab == 'tab-3':
        return dbc.Container([
            vs.kde_plot_selection_form,
            html.Hr(),
            vs.kde_static_plot if plot_type == 'static_plot' else vs.kde_interactive_plot if plot_type == 'interactable_plot' else dbc.Alert('Error: Invalid plot type selected', color='danger')
        ])
    elif tab == 'tab-4':
        return dbc.Container([vs.box_plot_container])
    elif tab == 'tab-5':
        return dbc.Container([vs.auroc_container])
    elif tab == 'tab-6':
        return dbc.Container([
            html.Hr(),
            html.H3("Custom Prediction Input Form"),
            cpf.custom_prediction_form
        ])


if __name__ == "__main__":
    app.run(debug=True)
