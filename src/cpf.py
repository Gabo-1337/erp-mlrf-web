# Third-party imports for web application
import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc

# Local application/library specific imports
import validator


# -------------------------------------------------------------------------------------------------------
# * Initializations

# * Global list to store the inputs
# * used as a temporary storage for the user inputs in CPF so when they save it as a file
# * it goes here and get sent to download_csv()
to_csv_inputs = []

# * temporary storage for the user inputs in CPF
# * this is the one that shows up in the table
table_csv_inputs = []

table_csv_inputs_column_names = ['Satisfaction Level', 'Number of Projects', 'Average Monthly Hours', 'Time Spent in Company', 'Salary', 'Department', 'OUTPUT']

# -------------------------------------------------------------------------------------------------------
# * Custom Prediction Forms
# * cpf means Custom Prediction forms

satisfaction_level_cpf_input = dbc.Row(
    [
        dbc.Label('Satisfaction Level', html_for='satisfaction_level_cpf', width=2),
        dbc.Col(
            dbc.Input(
                type='number',
                id='satisfaction_level_cpf',
                placeholder='Please input a number [ 1 - 100 ] or decimal values [ 0.01 - 0.99 ]',
                debounce=True,
                max=100,
            ),
            width=10,
        ),
    ],
    className='mb-3',
)


# -------------------------------------------------------------------------------------------------------
# * number_project_cpf_input

number_project_cpf_input = dbc.Row(
    [
        dbc.Label('Number of Projects', html_for='number_project_cpf', width=2),
        dbc.Col(
            dbc.Input(
                type='number',
                id='number_project_cpf',
                placeholder='Please toggle or input an integer between 1 and 10',
                debounce=True,
                min=1,
                max=10,
                step=1,
            ),
            width=10,
        ),
    ],
    className='mb-3',
)

number_project_cpf_input.validate = validator.validate_integer
number_project_cpf_input.invalid_feedback = 'Please toggle or input an integer between 1 and 10'

# -------------------------------------------------------------------------------------------------------
# * average_monthly_hours_cpf_input

average_monthly_hours_cpf_input = dbc.Row(
    [
        dbc.Label('Average Monthly Hours', html_for='average_monthly_hours_cpf', width=2),
        dbc.Col(
            dbc.Input(
                type='number',
                id='average_monthly_hours_cpf',
                placeholder='Please toggle or input an integer number between 1 and 310',
                debounce=True,
                min=1,
                max=310,
                step=1,
            ),
            width=10,
        ),
    ],
    className='mb-3',
)

average_monthly_hours_cpf_input.validate = validator.validate_amh_range
average_monthly_hours_cpf_input.invalid_feedback = 'Please toggle or input an integer number between 1 and 310'

# -------------------------------------------------------------------------------------------------------
# * time_spend_company_cpf_input

time_spend_company_cpf_input = dbc.Row(
    [
        dbc.Label('Time Spent in Company', html_for='time_spend_company_cpf', width=2),
        dbc.Col(
            dbc.Input(
                type='number',
                id='time_spend_company_cpf',
                placeholder='Please toggle or input an integer number between 1 and 10',
                debounce=True,
                min=1,
                max=10,
                step=1,
            ),
            width=10,
        ),
    ],
    className='mb-3',
)

time_spend_company_cpf_input.validate = validator.validate_integer
time_spend_company_cpf_input.invalid_feedback = 'Please toggle or input an integer number between 1 and 10'


# -------------------------------------------------------------------------------------------------------
# * salary_cpf_input

salary_cpf_input = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label('Salary', html_for='salary_cpf', width=2),
                dbc.Col(
                    dbc.Select(
                        id='salary_cpf',
                        options=[
                            {'label': 'Low', 'value': '1'},
                            {'label': 'Medium', 'value': '2'},
                            {'label': 'High', 'value': '3'},
                        ],
                    ),
                    width=10,
                ),
            ],
            className='mb-3',
        )
    ]
)

# -------------------------------------------------------------------------------------------------------
# * department_cpf_input

department_cpf_input = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label('Department', html_for='department_cpf', width=2),
                dbc.Col(
                    dbc.Select(
                        id='department_cpf',
                        options=[
                            {'label': 'IT', 'value': 'IT'},
                            {'label': 'Research and Development', 'value': 'RandD'},
                            {'label': 'Accounting', 'value': 'accounting'},
                            {'label': 'HR', 'value': 'hr'},
                            {'label': 'Management', 'value': 'management'},
                            {'label': 'Marketing', 'value': 'marketing'},
                            {'label': 'Product Management', 'value': 'product_mng'},
                            {'label': 'Sales', 'value': 'sales'},
                            {'label': 'Support', 'value': 'support'},
                            {'label': 'Technical', 'value': 'technical'},
                        ],
                    ),
                    width=10,
                ),
            ],
            className='mb-3',
        )
    ]
)

# -------------------------------------------------------------------------------------------------------
# * prints out the prediction
cpf_output = dbc.Row(
    [
        dbc.Label('Output', html_for='cpf_output', width=2),
        dbc.Col(
            dbc.Input(
                id='cpf_output',
                disabled=True
            ),
            width=10,
        ),
    ],
    className='mb-3',
)


# -------------------------------------------------------------------------------------------------------
# * prints out the prediction in the table
cpf_output_table = dbc.Row(
    [
        dbc.Label('User Inputs', html_for='cpf_output_table', width=2),
        dbc.Col(
            dash_table.DataTable(
                id='cpf_output_table',
                columns=[{'name': i, 'id': i} for i in table_csv_inputs_column_names],
                editable=False,
                style_cell_conditional=[
                    {
                        'if': {'column_id': i},
                        'textAlign': 'left'
                    } for i in ['Satisfaction Level', 'Number of Projects']
                ],
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(242, 242, 242)',
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(255, 255, 255)',
                    'color': 'black',
                    'border': '1px solid black',
                    'fontWeight': 'bold'
                },
                style_data={
                    'color': 'black',
                    'border': '1px solid gray',
                    'backgroundColor': 'white'
                },
            ),
            width=10,
        ),
    ],
    className='mb-3',
)


# -------------------------------------------------------------------------------------------------------
# * prints out all of the form and shows the output and the table
custom_prediction_form = dbc.Form(
    [
        satisfaction_level_cpf_input,
        number_project_cpf_input,
        average_monthly_hours_cpf_input,
        time_spend_company_cpf_input,
        salary_cpf_input,
        department_cpf_input,
        cpf_output,
        html.Div([
            dbc.Button('Submit', id='submit-button-id', color='primary', n_clicks=0, style={'margin-right': '10px'}),
            dbc.Button('Save inputs', id='save-button-id', n_clicks=0, style={'margin-right': '10px'}),
            dcc.Download(id="download-dataframe-csv"),
        ], style={'textAlign': 'center'}),
        html.Hr(),
        cpf_output_table
    ]
)