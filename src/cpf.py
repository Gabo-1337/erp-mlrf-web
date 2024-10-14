# Third-party imports for web application
import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc, Input, Output

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

table_csv_inputs_column_names = ['Age Group', 'Environment Satisfaction', 'Job Satisfaction', 'Relationship Satisfaction',
                'Performance Rating', 'Work-Life Balance', 'Job Involvement', 'Job Level', 'Over Time', 'Monthly Income', 
                'Years At Company', 'Total Working Years', 'Years SinceLast Promotion', 'OUTPUT']

table_csv_inputs_column_names_save_file = ['AgeGroup', 'EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction',
                'PerformanceRating', 'WorkLifeBalance', 'JobInvolvement', 'JobLevel', 'OverTime', 'MonthlyIncome', 
                'YearsAtCompany', 'TotalWorkingYears', 'YearsSinceLastPromotion', 'OUTPUT']

# -------------------------------------------------------------------------------------------------------
# * Custom Prediction Forms
# * cpf means Custom Prediction forms

env_satis_cpf_input = dbc.Row(
    [
        dbc.Label('Environment Satisfaction:', html_for='env_satis_cpf', width=2, id='env_satis_tt'),
        dbc.Col(
            dbc.Select(
                disabled=False,
                options=[
                    {'label': '0 - N/A', 'value': '0'},
                    {'label': '1 - Low', 'value': '1'},
                    {'label': '2 - Medium', 'value': '2'},
                    {'label': '3 - High', 'value': '3'},
                    {'label': '4 - Very High', 'value': '4'},
                ],
                id='env_satis_cpf',
                value='1',
            ),
            width=10,
        ),
        # dbc.Tooltip(
        #         'Different ways of obtaining this kind of data may subject to usage of other values: "1 - Low" could mean <60% in a statistical sense, or it could also mean 25% in another scenario, convert your values to the current selection for determining what to input here.',
        #         target="env_satis_tt",
        #         placement="left"
        #     ),
    ],
    className='mb-3',
)


# -------------------------------------------------------------------------------------------------------
# * number_project_cpf_input

job_satis_cpf_input = dbc.Row(
    [
        dbc.Label('Job Satisfaction:', html_for='job_satis_cpf', width=2, id='job_satis_tt'),
        dbc.Col(
            dbc.Select(
                options=[
                    {'label': '0 - N/A', 'value': '0'},
                    {'label': '1 - Low', 'value': '1'},
                    {'label': '2 - Medium', 'value': '2'},
                    {'label': '3 - High', 'value': '3'},
                    {'label': '4 - Very High', 'value': '4'},
                ],
                id='job_satis_cpf',
                value='1',
            ),
            width=10,
        ),
        # dbc.Tooltip(
        #         'Check the tab "Bar Charts" to know how to interpret the data you should input.',
        #         target="job_satis_tt",
        #         placement="top"
        # ),
    ],
    className='mb-3',
)

# number_project_cpf_input.validate = validator.validate_integer
# job_satis_cpf_input.invalid_feedback = 'Please toggle input'

# -------------------------------------------------------------------------------------------------------
# * rel_satis_cpf_input

rel_satis_cpf_input = dbc.Row(
    [
        dbc.Label('Relationship Satisfaction:', html_for='rel_satis_cpf', width=2, id='rel_satis_tt'),
        dbc.Col(
            dbc.Select(
                options=[
                    {'label': '0 - N/A', 'value': '0'},
                    {'label': '1 - Low', 'value': '1'},
                    {'label': '2 - Medium', 'value': '2'},
                    {'label': '3 - High', 'value': '3'},
                    {'label': '4 - Very High', 'value': '4'},
                ],
                id='rel_satis_cpf',
                value='1',
            ),
            width=10,
        ),
        # dbc.Tooltip(
        #         "Check the tab 'Bar Charts' to know how to interpret the data you should input.",
        #         target="rel_satis_tt",
        #         placement="top"
        # ),
    ],
    className='mb-3',
)

# average_monthly_hours_cpf_input.validate = validator.validate_amh_range
# rel_satis_cpf_input.invalid_feedback = 'Please toggle or input an integer number between 1 and 310'

# -------------------------------------------------------------------------------------------------------
# * perf_rating_cpf_input

perf_rating_cpf_input = dbc.Row(
    [
        dbc.Label('Performance Rating:', html_for='perf_rating_cpf', width=2, id='perf_rating_tt'),
        dbc.Col(
            dbc.Select(
                options=[
                    {'label': '0 - N/A', 'value': '0'},
                    {'label': '1 - Low', 'value': '1'},
                    {'label': '2 - Good', 'value': '2'},
                    {'label': '3 - Excellent', 'value': '3'},
                    {'label': '4 - Outstanding', 'value': '4'},
                ],
                id='perf_rating_cpf',
                value='1',
            ),
            width=10,
        ),
        # dbc.Tooltip(
        #         "Check the tab 'Bar Charts' to know how to interpret the data you should input.",
        #         target="perf_rating_tt",
        #         placement="top"
        # ),
    ],
    className='mb-3',
)

# -------------------------------------------------------------------------------------------------------
# * wlbal_cpf_input

wlbal_cpf_input = dbc.Row(
    [
        dbc.Label('Work-Life Balance:', html_for='wlbal_cpf', width=2, id='wlbal_tt'),
        dbc.Col(
            dbc.Select(
                options=[
                    {'label': '0 - N/A', 'value': '0'},
                    {'label': '1 - Bad', 'value': '1'},
                    {'label': '2 - Good', 'value': '2'},
                    {'label': '3 - Better', 'value': '3'},
                    {'label': '4 - Best', 'value': '4'},
                ],
                id='wlbal_cpf',
                value='1',
            ),
            width=10,
        ),
        # dbc.Tooltip(
        #         "Check the tab 'Bar Charts' to know how to interpret the data you should input.",
        #         target="wlbal_tt",
        #         placement="top"
        # ),
    ],
    className='mb-3',
)

# -------------------------------------------------------------------------------------------------------
# * job_inv_cpf_input

job_inv_cpf_input = dbc.Row(
    [
        dbc.Label('Job Involvement:', html_for='job_inv_cpf', width=2, id='job_inv_tt'),
        dbc.Col(
            dbc.Select(
                options=[
                    {'label': '0 - N/A', 'value': '0'},
                    {'label': '1 - Low', 'value': '1'},
                    {'label': '2 - Medium', 'value': '2'},
                    {'label': '3 - High', 'value': '3'},
                    {'label': '4 - Very High', 'value': '4'},
                ],
                id='job_inv_cpf',
                value='1',
            ),
            width=10,
        ),
        # dbc.Tooltip(
        #         "Check the tab 'Bar Charts' to know how to interpret the data you should input.",
        #         target="job_inv_tt",
        #         placement="top"
        # ),
    ],
    className='mb-3',
)

# -------------------------------------------------------------------------------------------------------
# * job_lev_cpf_input

job_lev_cpf_input = dbc.Row(
    [
        dbc.Label('Job Level:', html_for='job_lev_cpf', width=2, id='job_lev_tt'),
        dbc.Col(
            dbc.Select(
                options=[
                    {'label': '0 - N/A', 'value': '0'},
                    {'label': '1 - Entry Level', 'value': '1'},
                    {'label': '2 - Intermediate Level', 'value': '2'},
                    {'label': '3 - Experienced Level', 'value': '3'},
                    {'label': '4 - Advanced', 'value': '4'},
                    {'label': '5 - Expert', 'value': '5'},
                ],
                id='job_lev_cpf',
                value='1',
            ),
            width=10,
        ),
        # dbc.Tooltip(
        #         "Check the tab 'Bar Charts' to know how to interpret the data you should input.",
        #         target="job_lev_tt",
        #         placement="top"
        # ),
    ],
    className='mb-3',
)

# -------------------------------------------------------------------------------------------------------
# * age_group_cpf_input

age_group_cpf_input = dbc.Row(
    [
        dbc.Label('Age Group:', html_for='age_group_cpf', width=2, id='age_group_tt'),
        dbc.Col(
            dbc.Select(
                options=[
                    {'label': '0 - Near Retirement (60+)', 'value': 'a_gro_ret'},
                    {'label': '1 - Young Adult (18-30)', 'value': 'a_gro_ya'},
                    {'label': '2 - Adult (30-60)', 'value': 'a_gro_a'},
                ],
                id='age_group_cpf',
                value='a_gro_ya',
            ),
            width=10,
        ),
        # dbc.Tooltip(
        #         "Check the tab 'Bar Charts' to know how to interpret the data you should input.",
        #         target="age_group_tt",
        #         placement="top"
        # ),
    ],
    className='mb-3',
)

# -------------------------------------------------------------------------------------------------------
# * ot_cpf_input

ot_cpf_input = dbc.Row(
    [
        dbc.Label('Has Overtime:', html_for='ot_cpf', width=2, id='ot_tt'),
        dbc.Col(
            dbc.Select(
                options=[
                    {'label': '0 - N/A', 'value': '0'},
                    {'label': '1 - Yes', 'value': '1'},
                    {'label': '2 - No', 'value': '2'},
                ],
                id='ot_cpf',
                value='1',
            ),
            width=10,
        ),
        # dbc.Tooltip(
        #         "Check the tab 'Bar Charts' to know how to interpret the data you should input.",
        #         target="ot_tt",
        #         placement="top"
        # ),
    ],
    className='mb-3',
)

# -------------------------------------------------------------------------------------------------------
# * monthly_income_cpf_input

monthly_income_cpf_input = dbc.Row(
    [
        dbc.Label('Monthly Income:', html_for='monthly_income_cpf', width=2, id='monthly_income_tt'),
        dbc.Col(
            dbc.Input(
                type='number',
                id='monthly_income_cpf',
                disabled=False,
                placeholder='Please input monthly income',
                debounce=True,
                value='0',
                min=0,
                ),
            width=9,
        ),
        dbc.Col(
            dbc.Checklist(
                id='monthly_income_disable',
                options=[
                    {'label': 'N/A', 'value': 'disabled'},
                ],
                value=[],
            ),
        ),
        # dbc.Tooltip(
        #         "Check the tab 'Bar Charts' to know how to interpret the data you should input.",
        #         target="monthly_income_tt",
        #         placement="top"
        # ),
    ],
    className='mb-3',
)

monthly_income_cpf_input.validate = validator.validate_integer
monthly_income_cpf_input.invalid_feedback = 'Please only input number equal or more than 0 and less than 1000000'

# -------------------------------------------------------------------------------------------------------
# * yat_com_cpf_input

yat_com_cpf_input = dbc.Row(
    [
        dbc.Label('Years at Company:', html_for='yat_com_cpf', width=2, id='yat_com_tt'),
        dbc.Col(
            dbc.Input(
                type='number',
                id='yat_com_cpf',
                disabled=False,
                placeholder='Please input years at company',
                debounce=True,
                value='0',
                min=0,
                ),
            width=9,
        ),
        dbc.Col(
            dbc.Checklist(
                id='yat_com_disable',
                options=[
                    {'label': 'N/A', 'value': 'disabled'},
                ],
                value=[],
            ),
        ),
        # dbc.Tooltip(
        #         "Check the tab 'Bar Charts' to know how to interpret the data you should input.",
        #         target="yat_com_tt",
        #         placement="top"
        # ),
    ],
    className='mb-3',
)

yat_com_cpf_input.validate = validator.validate_integer
yat_com_cpf_input.invalid_feedback = 'Please only input number equal or more than 0 and less than 1000000'

# -------------------------------------------------------------------------------------------------------
# * totwork_years_cpf_input

totwork_years_cpf_input = dbc.Row(
    [
        dbc.Label('Years of Experience:', html_for='totwork_years_cpf', width=2, id='totwork_years_tt'),
        dbc.Col(
            dbc.Input(
                type='number',
                id='totwork_years_cpf',
                disabled=False,
                placeholder='Please input total years working',
                debounce=True,
                value='0',
                min=0,
                ),
            width=9,
        ),
        dbc.Col(
            dbc.Checklist(
                id='totwork_years_disable',
                options=[
                    {'label': 'N/A', 'value': 'disabled'},
                ],
                value=[],
            ),
        ),
        # dbc.Tooltip(
        #         "Check the tab 'Bar Charts' to know how to interpret the data you should input.",
        #         target="totwork_years_tt",
        #         placement="top"
        # ),
    ],
    className='mb-3',
)

totwork_years_cpf_input.validate = validator.validate_integer
totwork_years_cpf_input.invalid_feedback = 'Please only input number equal or more than 0 and less than 1000000'

# -------------------------------------------------------------------------------------------------------
# * ysl_promote_cpf_input

ysl_promote_cpf_input = dbc.Row(
    [
        dbc.Label('Years Since Last Promotion:', html_for='ysl_promote_cpf', width=2, id='ysl_promote_tt'),
        dbc.Col(
            dbc.Input(
                type='number',
                id='ysl_promote_cpf',
                disabled=False,
                placeholder='Please input years since last promotion',
                debounce=True,
                value='0',
                min=0,
                ),
            width=9,
        ),
        dbc.Col(
            dbc.Checklist(
                id='ysl_promote_disable',
                options=[
                    {'label': 'N/A', 'value': 'disabled'},
                ],
                value=[],
            ),
        ),
        # dbc.Tooltip(
        #         "Check the tab 'Bar Charts' to know how to interpret the data you should input.",
        #         target="ysl_promote_tt",
        #         placement="top"
        # ),
    ],
    className='mb-3',
)

ysl_promote_cpf_input.validate = validator.validate_integer
ysl_promote_cpf_input.invalid_feedback = 'Please only input number equal or more than 0 and less than 1000000'

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
cpf_output_table = dbc.Row(
    [
        html.Div(
            dash_table.DataTable(
                id='cpf_output_table',
                columns=[{'name': i, 'id': i} for i in table_csv_inputs_column_names],
                editable=False,
                style_cell_conditional=[
                    {
                        'if': {'column_id': i},
                        'textAlign': 'left'
                    }
                    for i in ['Generation_Group_Boomers', 'Generation_Group_Generation X']
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
                    'fontWeight': 'bold',
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_data={
                    'color': 'black',
                    'border': '1px solid gray',
                    'backgroundColor': 'white',
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_cell={
                    'minWidth': '150px', 'width': 'auto', 'maxWidth': '300px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'whiteSpace': 'normal'
                },
                fixed_rows={'headers': True},  # Make headers stay persistent
                style_table={'height': '400px', 'overflowY': 'auto'}  # Enable vertical scrolling
            ),
            # style={'height': '400px', 'overflowY': 'scroll'}  # Ensure the container scrolls
        ),
    ],
    className='mb-3',
)

# -------------------------------------------------------------------------------------------------------
# * prints out all of the form and shows the output and the table
custom_prediction_form = dbc.Form(
    [
        env_satis_cpf_input,
        job_satis_cpf_input,
        rel_satis_cpf_input,
        perf_rating_cpf_input,
        wlbal_cpf_input,
        job_inv_cpf_input,
        job_lev_cpf_input,
        age_group_cpf_input,
        ot_cpf_input,
        monthly_income_cpf_input,
        yat_com_cpf_input,
        totwork_years_cpf_input,
        ysl_promote_cpf_input,
        cpf_output,
        html.Div([
            dbc.Button('Submit', id='submit_button_id', color='primary', n_clicks=0, style={'margin-right': '10px'}),
            dbc.Button('Save inputs', id='save_button_id', n_clicks=0, style={'margin-right': '10px'}),
            dcc.Download(id="download_dataframe_csv"),
        ], style={'textAlign': 'center'}),
        html.Hr(),
        cpf_output_table
    ]
)