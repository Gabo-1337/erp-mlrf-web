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
server = app.server

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
        dcc.Tabs(id="tabs", value='tab-7', children=[
            dcc.Tab(label='Prediction Form', value='tab-7'),
            dcc.Tab(label='Bar Charts', value='tab-1'),
            dcc.Tab(label='Correlation Heatmap', value='tab-2'),
            dcc.Tab(label='Confusion Matrix', value='tab-3'),
            dcc.Tab(label='KDE Plot', value='tab-4'),
            dcc.Tab(label='Box Plot', value='tab-5'),
            dcc.Tab(label='AUROC Graph', value='tab-6'),
        ]),
        html.Div(id='tabs-content')
    ]
)

# validator for the cpf inputs
@app.callback(
    [
     Output("monthly_income_cpf", "className"),
     Output("yat_com_cpf", "className"),
     Output("totwork_years_cpf", "className"),
     Output("ysl_promote_cpf", "className")
    ],
    [
     Input("monthly_income_cpf", "value"),
     Input("yat_com_cpf", "value"),
     Input("totwork_years_cpf", "value"),
     Input("ysl_promote_cpf", "value")
    ]
)
def update_classnames(monthly_income, yat_com, totworks_years, ysl_promote):
    return [
        "is-valid" if vd.validate_integer(monthly_income) else "is-invalid",
        "is-valid" if vd.validate_integer(yat_com) else "is-invalid",
        "is-valid" if vd.validate_integer(totworks_years) else "is-invalid",
        "is-valid" if vd.validate_integer(ysl_promote) else "is-invalid"
    ]

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
     Input("save_button_id", "n_clicks"),
    ],
    [
     # These states are the inputs for making predictions
     State('env_satis_cpf', 'value'),
     State('job_satis_cpf', 'value'),
     State('rel_satis_cpf', 'value'),
     State('perf_rating_cpf', 'value'),
     State('wlbal_cpf', 'value'),
     State('job_inv_cpf', 'value'),
     State('job_lev_cpf', 'value'),
     State('age_group_cpf', 'value'),
     State('ot_cpf', 'value'),
     State('monthly_income_cpf', 'value'),
     State('yat_com_cpf', 'value'),
     State('totwork_years_cpf', 'value'),
     State('ysl_promote_cpf', 'value'),
     State('session_user_input', 'data')
    ]
)

def predict_or_save(n_clicks_submit, n_clicks_save, env_s, j_stf, r_sts, pf_rt, wl_bl, j_inv, j_lvl, a_gro, ovr_t, m_inc, y_com, tw_yr, y_prm, session_data):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if session_data is None:
        session_data = {'to_csv_inputs': [], 'table_csv_inputs': []}

    if button_id == "submit_button_id" and n_clicks_submit:
        # Check if any input is blank
        # if not all([m_inc, y_com, tw_yr, y_prm]):
        #     return "ERROR: Missing input or wrong input.", no_update, no_update, session_data

        # this one have 3 return values, so I arranged them this way and they have to be this way. see the last return part on bpred for reference.
        pred_output, pred_to_csv, gen_g_string = bp.make_prediction(env_s, j_stf, r_sts, pf_rt, wl_bl, j_inv, j_lvl, a_gro, ovr_t, m_inc, y_com, tw_yr, y_prm)
        # Store output for to csv / to save file
        session_data['to_csv_inputs'].append([gen_g_string, env_s, j_stf, r_sts, pf_rt, wl_bl, j_inv, j_lvl, ovr_t, m_inc, y_com, tw_yr, y_prm, pred_to_csv])
        # Store output for the table / used for displaying the user inputs in table
        session_data['table_csv_inputs'].append([gen_g_string, env_s, j_stf, r_sts, pf_rt, wl_bl, j_inv, j_lvl, ovr_t, m_inc, y_com, tw_yr, y_prm, pred_to_csv])
        # Convert each list in cpf.table_csv_inputs to a dictionary that is going to be used in showing user inputs
        output_table_data = [dict(zip(cpf.table_csv_inputs_column_names, row)) for row in session_data['table_csv_inputs']]
        return pred_output, output_table_data, no_update, session_data

    elif button_id == "save_button_id" and n_clicks_save:
        df_output_table_data = pd.DataFrame(session_data['table_csv_inputs'], columns=cpf.table_csv_inputs_column_names_save_file)
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
        return dbc.Container([vs.cfm_container])
    elif tab == 'tab-4':
        if session_data is not None:
            session_data['to_csv_inputs'] = []
            session_data['table_csv_inputs'] = []
        return dbc.Container([vs.kde_plot_container])
    elif tab == 'tab-5':
        if session_data is not None:
            session_data['to_csv_inputs'] = []
            session_data['table_csv_inputs'] = []
        return dbc.Container([vs.box_plot_container])
    elif tab == 'tab-6':
        if session_data is not None:
            session_data['to_csv_inputs'] = []
            session_data['table_csv_inputs'] = []
        return dbc.Container([vs.auroc_container])
    elif tab == 'tab-7':
        return dbc.Container([
            html.Hr(),
            html.P(
                [
                html.H3("Custom Prediction Input Form"),
                html.Span(
                    "Hover here to know what to input and how your data can be interpreted.",
                    id="my-target",
                    style={"cursor": "pointer"},
                    ),
                ]
            ),
            dbc.Tooltip(
                'Different ways of obtaining data may subject to usage of other values: "1 - Low" could mean <60% in a statistical sense, or it could also mean 25% in another scenario, convert your values to the current selection for determining what to input here. WARNING: Disabling values will change those values to default to 0, limit disabling 1-3 values only to avoid false results.',
                target="my-target",
                placement="left"
            ),
            cpf.custom_prediction_form
        ])

# -------------------------------------------------------------------------------------------------------
# * Disabling inputs in cpf.py
# -------------------------------------------
# * Combined Callback for Multiple Sliders
@app.callback(
    # Output('env_satis_cpf', 'disabled'),
    # Output('job_satis_cpf', 'disabled'),
    # Output('rel_satis_cpf', 'disabled'),
    # Output('perf_rating_cpf', 'disabled'),
    # Output('wlbal_cpf', 'disabled'),
    # Output('job_inv_cpf', 'disabled'),
    # Output('job_lev_cpf', 'disabled'),
    # Output('age_group_cpf', 'disabled'),
    # Output('ot_cpf', 'disabled'),
    Output('monthly_income_cpf', 'disabled'),
    Output('yat_com_cpf', 'disabled'),
    Output('totwork_years_cpf', 'disabled'),
    Output('ysl_promote_cpf', 'disabled'),
    # [Input('env_satis_disable', 'value'),
    #  Input('job_satis_disable', 'value'),
    #  Input('rel_satis_disable', 'value'),
    #  Input('perf_rating_disable', 'value'),
    #  Input('wlbal_disable', 'value'),
    #  Input('job_inv_disable', 'value'),
    #  Input('job_lev_disable', 'value'),
    # [Input('age_group_disable', 'value'),
    #  Input('ot_disable', 'value'),
    [Input('monthly_income_disable', 'value'),
     Input('yat_com_disable', 'value'),
     Input('totwork_years_disable', 'value'),
     Input('ysl_promote_disable', 'value')]
)
# def update_sliders_disabled(env_satis_disabled, job_satis_disabled, rel_satis_disabled, perf_rating_disabled, wlbal_disabled, job_inv_disabled, job_lev_disabled, age_group_disabled, ot_disabled, monthly_income_disabled, yat_com_disabled, totwork_years_disabled, ysl_promote_disabled):
def update_sliders_disabled(monthly_income_disabled, yat_com_disabled, totwork_years_disabled, ysl_promote_disabled):
    return (
        # 'disabled' in env_satis_disabled,
        # 'disabled' in job_satis_disabled,
        # 'disabled' in rel_satis_disabled,
        # 'disabled' in perf_rating_disabled,
        # 'disabled' in wlbal_disabled,
        # 'disabled' in job_inv_disabled,
        # 'disabled' in job_lev_disabled,
        # 'disabled' in age_group_disabled,
        # 'disabled' in ot_disabled,
        'disabled' in monthly_income_disabled,
        'disabled' in yat_com_disabled,
        'disabled' in totwork_years_disabled,
        'disabled' in ysl_promote_disabled
    )

# @app.callback(
#     [Output('age_group_cpf', 'value')],
#     [Input('age_group_disable', 'value')],
#     [State('age_group_cpf', 'value')]
# )
# def m_inc_disable(a_gro_dis, a_gro):
#     return (
#         [0] if a_gro_dis else [a_gro]
#     )

@app.callback(
    [Output('monthly_income_cpf', 'value')],
    [Input('monthly_income_disable', 'value')],
    [State('monthly_income_cpf', 'value')]
)
def m_inc_disable(mon_inc_dis, mon_inc):
    return (
        [0] if mon_inc_dis else [mon_inc]
    )

@app.callback(
    [Output('yat_com_cpf', 'value')],
    [Input('yat_com_disable', 'value')],
    [State('yat_com_cpf', 'value')]
)
def yat_com_disable(yat_com_dis, yat_com):
    return (
        [0] if yat_com_dis else [yat_com]
    )

@app.callback(
    [Output('totwork_years_cpf', 'value')],
    [Input('totwork_years_disable', 'value')],
    [State('totwork_years_cpf', 'value')]
)
def tw_yr_disable(tw_yr_dis, tw_yr):
    return (
        [0] if tw_yr_dis else [tw_yr]
    )

@app.callback(
    [Output('ysl_promote_cpf', 'value')],
    [Input('ysl_promote_disable', 'value')],
    [State('ysl_promote_cpf', 'value')]
)
def yrs_prm_disable(yrs_prm_dis, yrs_prm):
    return (
        [0] if yrs_prm_dis else [yrs_prm]
    )
    
# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=False)