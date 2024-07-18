# Standard library imports
import os

# Third-party imports for data manipulation
import numpy as np
import pandas as pd

# Third-party imports for visualization
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageOps

# Third-party imports for machine learning
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Third-party imports for web application
from dash import dcc, html
import dash_bootstrap_components as dbc


# -------------------------------------------------------------------------------------------------------
# * initialization

# * dataset initalization
data = pd.read_csv('https://raw.githubusercontent.com/CS-DREAM-TEAM/assets/main/HR_comma_sep.csv')

# * variable initializations
left_company = data[data['left'] == 1]
stay_company = data[data['left'] == 0]

# * One hot encoding: Dummy Variable for the Department
inputs = data[['satisfaction_level', 'number_project', 'average_montly_hours', 'time_spend_company', 'Department', 'salary']]
target = data.left

inputs.replace({'salary': {'low': 1, 'medium': 2, 'high': 3}}, inplace=True)

dep_dummies = pd.get_dummies(data['Department'])
df_with_dummies = pd.concat([inputs, dep_dummies], axis='columns')
df_with_dummies.drop('Department', axis='columns', inplace=True)

x = df_with_dummies
y = target

# * css / ui design
external_stylesheets = [
    {
        'href': ('https://fonts.googleapis.com/css2?' 'family=Lato:wght@400;700&display=swap'),
        'rel': 'stylesheet',
    },
]


# -------------------------------------------------------------------------------------------------------
# * BAR PLOTS

# Initialization
df_visuals = data.copy()

# ===========================================================================
# * TAB 1 Satisfaction Level bar plot

# Create satisfaction bins and labels
satisfaction_bins = [0.0, 0.25, 0.50, 0.75, 1.00]
satisfaction_labels = ['0/% - 25/%', '25/% - 50/%', '50/% - 75/%', '75/% - 100/%']

df_visuals['satisfaction_Group'] = pd.cut(df_visuals['satisfaction_level'], bins=satisfaction_bins, labels=satisfaction_labels, right=False)
satisfaction_grouped_df = df_visuals.groupby(['satisfaction_Group', 'left'], observed=True).size().unstack(fill_value=0)

# Create the bar chart
satis_trace_stay = go.Bar(x=satisfaction_grouped_df.index, y=satisfaction_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
satis_trace_left = go.Bar(x=satisfaction_grouped_df.index, y=satisfaction_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

satis_layout = go.Layout(
    title='Employee status by Satisfaction Level',
    xaxis=dict(title='Satisfaction Level'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

satisfaction_bins_fig = go.Figure(data=[satis_trace_stay, satis_trace_left], layout=satis_layout)

satisfaction_bin_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=satisfaction_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Satisfaction Level')),
                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.P("The bar chart visually compares the employment status of individuals based on their satisfaction level. It consists of two sets of bars:"),
                    html.Ul([
                        html.Li([
                            html.Strong('Stayed Employees (Blue Bars):'),
                            html.Ul([
                                html.Li('These represent employees who remained with the company.'),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Left Employees (Orange Bars):'),
                            html.Ul([
                                html.Li('These represent employees who left the company.'),
                            ])
                        ]),
                    ]),
                    html.P("The x-axis is labeled with satisfaction level ranges (e.g., 0-25%, 25-50%, etc.), and the y-axis represents the count of employees."),

                    html.H5(html.Strong('Employee Status and Satisfaction Level:')),
                    html.Ul([
                        html.Li([
                            html.Strong('Above 50% Satisfaction:'),
                            html.Ul([
                                html.Li('The blue bars dominate in this range, indicating that employees with satisfaction levels above 50% are more likely to stay with the company.'),
                                html.Li('The ratio of stay to leave is favorable, as the blue bars significantly exceed the orange bars.'),
                            ])
                        ]),
                        
                        html.Li([
                            html.Strong('Below 50% Satisfaction:'),
                            html.Ul([
                                html.Li('Conversely, for individuals with satisfaction levels below 50%, the orange bars are taller than the blue bars.'),
                                html.Li('This suggests that employees with lower satisfaction levels are more likely to leave the company.'),
                            ])
                        ]),
                    ]),
                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li('Employees with satisfaction levels above 50% are more likely to stay with the company.'),
                        html.Li('Individuals reporting less than 50% satisfaction tend to leave the company.'),
                        html.Li('Fostering a positive work environment and addressing employee concerns can improve satisfaction and retention rates.'),
                    ]),
                ])
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
    ],
)

# ===========================================================================
# * TAB 2 Work Evaluation bar plot

# Create satisfaction bins and labels
last_evaluation_bins = [0.0, 0.25, 0.50, 0.75, 1.00]
last_evaluation_labels = ['0/% - 25/%', '25/% - 50/%', '50/% - 75/%', '75/% - 100/%']

df_visuals['last_evaluation_Group'] = pd.cut(df_visuals['last_evaluation'], bins=last_evaluation_bins, labels=last_evaluation_labels, right=False)
work_eval_grouped_df = df_visuals.groupby(['last_evaluation_Group', 'left'], observed=True).size().unstack(fill_value=0)
# Create the bar chart
work_eval_trace_stay = go.Bar(x=work_eval_grouped_df.index, y=work_eval_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
work_eval_trace_left = go.Bar(x=work_eval_grouped_df.index, y=work_eval_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

work_eval_layout = go.Layout(
    title='Employee status by Work Performance Evaluation',
    xaxis=dict(title='Last Evaluation Performance'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

work_eval_bins_fig = go.Figure(data=[work_eval_trace_stay, work_eval_trace_left], layout=work_eval_layout)

work_eval_bin_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=work_eval_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Work Evaluation')),
                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.P("The bar chart presents data on the employment status of individuals categorized by their last work performance evaluation."),
                    html.P("The x-axis represents the range of last evaluation scores, divided into three groups: 25%-50%, 50%-75%, and 75%-100%. The y-axis indicates the count of employees."),
                    html.P("There are two sets of bars representing different employment statuses: 'Stay(0)' in blue, indicating employees who have remained with the company, and 'Left(1)' in orange, representing those who have left."),

                    html.H5(html.Strong('Employee Status and Work Evaluation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('25%-50% Evaluation Range:'),
                            html.Ul([
                                html.Li("A small number of employees who stayed fall into this range, while even fewer employees who left are in this category."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('50%-75% Evaluation Range:'),
                            html.Ul([
                                html.Li("There's a significant number of retained employees with evaluations within this range compared to a smaller count for those who left."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('75%-100% Evaluation Range:'),
                            html.Ul([
                                html.Li("Many employees who stayed have high evaluation scores in this bracket."),
                                html.Li("Interestingly, there's also a noticeable count of employees who left despite having high evaluations."),
                            ])
                        ]),
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li("Most retained employees fall within the middle to high range of work performance evaluations."),
                        html.Li("High last evaluation scores don't guarantee retention; some high-performing individuals still leave."),
                        html.Li("The minimal difference between the average last evaluation scores of retained employees (0.715473) and those who left (0.718113) suggests that last evaluation alone may not significantly impact retention decisions."),
                    ]),
                ])
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
    ],
)

# ===========================================================================\
# * TAB 3 Number of Projects plot

number_project_bins = [0, 2, 4, 6, 8, 10]
number_project_labels = ['0 - 2', '2 - 4', '4 - 6', '6 - 8', '8 - 10']

df_visuals['number_project_Group'] = pd.cut(df_visuals['number_project'], bins=number_project_bins, labels=number_project_labels, right=False)
number_project_grouped_df = df_visuals.groupby(['number_project_Group', 'left'], observed=True).size().unstack(fill_value=0)

num_proj_trace_stay = go.Bar(x=number_project_grouped_df.index, y=number_project_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
num_proj_trace_left = go.Bar(x=number_project_grouped_df.index, y=number_project_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

num_proj_layout = go.Layout(
    title='Employee status by Number of Projects',
    xaxis=dict(title='Number of Projects'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

num_proj_bins_fig = go.Figure(data=[num_proj_trace_stay, num_proj_trace_left], layout=num_proj_layout)

num_proj_bin_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=num_proj_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.Div([
                        html.H4(html.Strong('Explanation: Employment Status by Number of Projects')),
                        html.P("The bar chart visually represents the relationship between the number of projects completed by employees and their employment status (whether they stayed or left the company)."),

                        html.H5(html.Strong('Bar Chart Interpretation:')),
                        html.Ul([
                            html.Li([
                                html.Strong('2-4 Projects:'),
                                html.Ul([
                                    html.Li("The blue bar (representing employees who stayed) is significantly higher than the orange bar (representing those who left). This suggests that employees with 2-4 projects are more likely to stay with the company."),
                                ])
                            ]),
                            html.Li([
                                html.Strong('4-6 Projects:'),
                                html.Ul([
                                    html.Li("The blue bar remains higher than the orange bar, indicating higher retention for employees with 4-6 projects compared to those with 2-4 projects."),
                                ])
                            ]),
                            html.Li([
                                html.Strong('6-8 Projects:'),
                                html.Ul([
                                    html.Li("The orange bar is higher than the blue bar, implying that employees who completed 6-8 projects are more likely to leave the company."),
                                ])
                            ]),
                        ]),

                        html.H5(html.Strong('Conclusion:')),
                        html.P("High project involvement may lead to increased attrition, possibly due to burnout or other factors."),
                    ])
                ])
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
    ],
)

# ===========================================================================
# * TAB 4 Average Monthly Hours

average_montly_hours_bins = [0, 100, 200, 300, 320]
average_montly_hours_labels = ['0 - 100', '100 - 200', '200 - 300', '300 - 310+']

df_visuals['average_montly_hours_Group'] = pd.cut(df_visuals['average_montly_hours'], bins=average_montly_hours_bins, labels=average_montly_hours_labels, right=False)
amh_grouped_df = df_visuals.groupby(['average_montly_hours_Group', 'left'], observed=True).size().unstack(fill_value=0)

amh_trace_stay = go.Bar(x=amh_grouped_df.index, y=amh_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
amh_trace_left = go.Bar(x=amh_grouped_df.index, y=amh_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

amh_layout = go.Layout(
    title='Employee status by Work Monthly Hours',
    xaxis=dict(title='Average Monthly Hours'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

amh_bins_fig = go.Figure(data=[amh_trace_stay, amh_trace_left], layout=amh_layout)

amh_bin_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=amh_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Work Monthly Hours')),
                    html.P("The bar chart visually represents the relationship between the average monthly hours worked by employees and their employment status (whether they stayed or left the company)."),

                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('0 - 100 Hours:'),
                            html.Ul([
                                html.Li("The blue bar (representing employees who stayed) is significantly higher than the orange bar (representing those who left). All 19 individuals in this category have stayed with the company."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('100 - 200 Hours:'),
                            html.Ul([
                                html.Li("The blue bar is considerably longer than the orange bar suggesting a high retention."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('200 - 300 Hours:'),
                            html.Ul([
                                html.Li("Similar to the previous category, the bars suggest high retention."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('300 - 310+ Hours:'),
                            html.Ul([
                                html.Li("The orange bar is dramatically higher than the blue bar, indicating that all 170 individuals who worked these extremely high average monthly hours left the company."),
                            ])
                        ]),
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.P("Employees working very high average monthly hours (300-310+) tend to leave the company, while those working fewer hours have higher retention rates. This pattern may highlight issues related to work-life balance or job satisfaction among those with excessive workloads."),
                ])
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
    ],
)

# ===========================================================================
# * TAB 5 Time Spend in Company

time_spend_company_bins = [0, 2, 4, 6, 8, 10]
time_spend_company_labels = ['0 - 2', '2 - 4', '4 - 6', '6 - 8', '8 - 10']

df_visuals['time_spend_company_Group'] = pd.cut(df_visuals['time_spend_company'], bins=time_spend_company_bins, labels=time_spend_company_labels, right=False)
time_spend_company_grouped_df = df_visuals.groupby(['time_spend_company_Group', 'left'], observed=True).size().unstack(fill_value=0)

tsc_trace_stay = go.Bar(x=time_spend_company_grouped_df.index, y=time_spend_company_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
tsc_trace_left = go.Bar(x=time_spend_company_grouped_df.index, y=time_spend_company_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

tsc_layout = go.Layout(
    title='Employee status by # of hours completed in the Company',
    xaxis=dict(title='Time Spent in Company'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

tsc_bins_fig = go.Figure(data=[tsc_trace_stay, tsc_trace_left], layout=tsc_layout)

tsc_bin_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=tsc_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Time Spend in Company')),
                    html.P("The bar chart visually represents the relationship between the number of hours completed (years in the company) by employees and their employment status (whether they stayed or left the company)."),

                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('2-4 Hours Completed:'),
                            html.Ul([
                                html.Li("The blue bar (representing employees who stayed) is highest in this category."),
                                html.Li("Employees who have spent 2-4 hours completed in the company tend to stay."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('4-6 Hours Completed:'),
                            html.Ul([
                                html.Li("The orange bar (representing employees who left) is similar in height to the blue bar."),
                                html.Li("Employees completing 4-6 hours completed also exhibit a moderate leave rate."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('6-8 Hours Completed:'),
                            html.Ul([
                                html.Li("The orange bar (representing employees who left) is lowest for this range."),
                                html.Li("Employees who have spent 6-8 hours completed in the company exhibit very low leave rate."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('8-10 Hours Completed:'),
                            html.Ul([
                                html.Li("Similar to the 6-8 hour range, the orange bar remains low."),
                                html.Li("Employees completing 8-10 hours completed also have a low leave rate."),
                            ])
                        ]),
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.P("Employees completing 2-4, 6-8, and 8-10 hours completed have the highest retention rates."),
                ])
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
    ],
)

# ===========================================================================
# * TAB 6 Department bar plot

department_left_total = left_company.groupby('Department')['left'].count()
department_stay_total = stay_company.groupby('Department')['left'].count()

department_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(
                    figure={
                        'data': [
                            {
                                'x': department_stay_total.index,
                                'y': department_stay_total.values,
                                'type': 'bar',
                                'name': 'Retained(0)',
                            },
                            {
                                'x': department_left_total.index,
                                'y': department_left_total.values,
                                'type': 'bar',
                                'name': 'Left(1)',
                            },
                        ],
                        'layout': {
                            'title': 'Department',
                            'width': 600,
                            'height': 449,
                        },
                    },
                    style={'border': '1px solid black', 'margin': '10px'},
                ),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Department')),
                    html.P("The bar chart visually represents the employment status categorized by department within a company. Let's break down the interpretation:"),
                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('IT:'),
                            html.P('A moderate number of employees stayed compared to those who left.'),
                        ]),
                        html.Li([
                            html.Strong('RandD (Research and Development):'),
                            html.P('More employees stayed than left.'),
                        ]),
                        html.Li([
                            html.Strong('Accounting:'),
                            html.P('A slightly higher number of employees stayed than left.'),
                        ]),
                        html.Li([
                            html.Strong('HR (Human Resources):'),
                            html.P('Similar numbers of employees stayed and left.'),
                        ]),
                        html.Li([
                            html.Strong('Management:'),
                            html.P('Significantly more employees stayed than left.'),
                        ]),
                        html.Li([
                            html.Strong('Marketing:'),
                            html.P('More employees stayed than left.'),
                        ]),
                        html.Li([
                            html.Strong('Product_mng (Product Management):'),
                            html.P('More employees stayed than left, with a small difference between the other groups.'),
                        ]),
                        html.Li([
                            html.Strong('Sales:'),
                            html.P('The highest number of both staying and leaving; however, the number that left is notably high compared to other departments.'),
                        ]),
                        html.Li([
                            html.Strong('Support:'),
                            html.P('A large number of stays with a significant amount also leaving; Third-highest turnover after Technical.'),
                        ]),
                        html.Li([
                            html.Strong('Technical:'),
                            html.P('High retention rate but also a high turnover rate; follows sales in both aspects.'),
                        ]),
                    ]),
                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li('While sales have the highest retention rate among all departments, it concurrently has the highest turnover rate.'),
                        html.Li('Technical and support departments also show substantial numbers in both retention and turnover.'),
                        html.Li('Management shows an exceptionally high retention rate with very few departures.'),
                        html.Li('Departments like HR, accounting, marketing, and product management exhibit more balance between stayers and leavers but still lean towards higher retention overall.'),
                    ]),
                ])
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
    ]
)

# ===========================================================================
# * TAB 7 salary bar plot

salary_left_total = left_company.groupby('salary')['left'].count()
salary_stay_total = stay_company.groupby('salary')['left'].count()

salary_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(
                    figure={
                        'data': [
                            {
                                'x': salary_stay_total.index,
                                'y': salary_stay_total.values,
                                'type': 'bar',
                                'name': 'Retained(0)',
                            },
                            {
                                'x': salary_left_total.index,
                                'y': salary_left_total.values,
                                'type': 'bar',
                                'name': 'Left(1)',
                            },
                        ],
                        'layout': {
                            'title': 'Salary',
                            'width': 600,
                            'height': 449,
                        },
                    },
                    style={'border': '1px solid black', 'margin': '10px'},
                ),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Salary')),
                    html.P("The bar chart visually represents the relationship between employee retention and turnover within three distinct salary ranges: high, low, and medium. Let's break down the interpretation:"),
                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('High Salary:'),
                            html.Ul([
                                html.Li('A very small number of employees have left [ Left(1) ] compared to a significantly larger number who have stayed [ Stay(0) ].'),
                                html.Li('High salary employees demonstrate the lowest leave rate.'),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Medium Salary:'),
                            html.Ul([
                                html.Li('Similar to the low salary range, there is a higher count of employees who have left [ Left(1) ] compared to those who have stayed [ Stay(0) ].'),
                                html.Li('Medium salary employees shows a moderate leave rate.'),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Low Salary:'),
                            html.Ul([
                                html.Li('The highest number of employees have left [ Left(1) ] in this category.'),
                                html.Li('Low salary employees have the highest leave rate.'),
                            ])
                        ]),
                    ]),
                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li('Employees with low salaries shows the highest leave rate.'),
                        html.Li('Medium salary employees also experience turnover, but to a lesser extent.'),
                        html.Li('High salary employees have the lowest leave rate and can be considered to have the highest retention ratio.'),
                        html.Li('Proper compensation is crucial for retaining employees; competitive pay should be a priority.'),
                    ]),
                ])
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
    ],
)

# ===========================================================================
# * TAB 8-9 Excluded Variables

work_acc_grouped_df = df_visuals.groupby(['Work_accident', 'left'], observed=True).size().unstack(fill_value=0)
promotion5yrs_grouped_df = df_visuals.groupby(['promotion_last_5years', 'left'], observed=True).size().unstack(fill_value=0)

work_acc_trace_stay = go.Bar(x=work_acc_grouped_df.index, y=work_acc_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
work_acc_trace_left = go.Bar(x=work_acc_grouped_df.index, y=work_acc_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

promotion5yrs_trace_stay = go.Bar(x=promotion5yrs_grouped_df.index, y=promotion5yrs_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
promotion5yrs_trace_left = go.Bar(x=promotion5yrs_grouped_df.index, y=promotion5yrs_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

work_acc_layout = go.Layout(
    title='Employee status by Work Accident',
    xaxis=dict(title='Work Accident'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

promotion5yrs_layout = go.Layout(
    title='Employee status by receiving Promotion from the last 5 years',
    xaxis=dict(title='Promotion last 5 years'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

work_acc_bins_fig = go.Figure(data=[work_acc_trace_stay, work_acc_trace_left], layout=work_acc_layout)
promotion5yrs_bins_fig = go.Figure(data=[promotion5yrs_trace_stay, promotion5yrs_trace_left], layout=promotion5yrs_layout)

excluded_vars_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(
                    figure=work_acc_bins_fig, 
                    style={'border': '1px solid black', 'margin': '10px'}
                ),
                html.Div([
                    html.H4(html.Strong('Explanation: Excluding WORK_ACCIDENT Variable')),
                    html.P("We made the decision not to include the WORK_ACCIDENT variable in our retention model. Here are the reasons why:"),
                    html.Ul([
                        html.Li([
                            html.Strong('Information Gain:'),
                            html.Ul([
                                html.Li('The information gain from the WORK_ACCIDENT variable is negligible.'),
                                html.Li('Including it would likely introduce noise or outliers to our system.'),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Impact on Retention:'),
                            html.Ul([
                                html.Li("Work accidents are rare. Using pandas' mean method, we found that the mean of respective employees' work accident status is 0.175009 for retained employees and 0.047326 for those who left."),
                                html.Li('Consequently, their impact on predicting retention is minimal.'),
                            ])
                        ]),
                    ]),
                    html.P("In summary, we consider these factors negligible for predicting employee retention."),
                    html.P("But it is worth showcasing the ratio of work accidents in the company, which is shown in the left side of the screen."),
                ])
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
        html.Hr(),
        html.Div(
            children=[
                dcc.Graph(
                    figure=promotion5yrs_bins_fig, 
                    style={'border': '1px solid black', 'margin': '10px'}
                ),
                html.Div([
                    html.H4(html.Strong('Explanation: Excluding promotion_last_5years Variable')),
                    html.P("We made the decision not to include the promotion_last_5years variable in our retention model. Here are the reasons why:"),
                    html.Ul([
                        html.Li([
                            html.Strong('Information Gain:'),
                            html.Ul([
                                html.Li('The information gain from the promotion_last_5years variable is negligible.'),
                                html.Li('Including it would likely introduce noise or outliers to our system.'),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Impact on Retention:'),
                            html.Ul([
                                html.Li("Promotions are very rare. Using pandas' mean method, we found that the mean of respective employees' promotion status is 0.026251 for retained employees and 0.005321 for those who left."),
                                html.Li('Consequently, their impact on predicting retention is minimal.'),
                            ])
                        ]),
                    ]),
                    html.P("In summary, we consider these factors negligible for predicting employee retention."),
                    html.P("But it is worth showcasing the ratio of promotions happened on the last 5 years in the company, which is shown in the bar graph in the left side of the screen."),
                ])
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
    ],
)

# ! ==========================================================================
# ! BAR CHART TABS

tab1 = dbc.Tab(satisfaction_bin_chart_container, label='Overall Satisfaction')
tab2 = dbc.Tab(work_eval_bin_chart_container, label='Work Evaluation')
tab3 = dbc.Tab(num_proj_bin_chart_container, label='Number of Projects')
tab4 = dbc.Tab(amh_bin_chart_container, label='Average Monthly Hours')
tab5 = dbc.Tab(tsc_bin_chart_container, label='Time Spend in Company')
tab6 = dbc.Tab(department_chart_container, label='Department')
tab7 = dbc.Tab(salary_chart_container, label='Salary')
tab89 = dbc.Tab(excluded_vars_chart_container, label='Excluded Variables')
tabs = dbc.Card(dbc.Tabs([tab1, tab2,tab3,tab4,tab5,tab6,tab7,tab89]))

bar_plot_selection_form = dbc.Container(
    [
        html.Hr(),
        dbc.Row([
            dbc.Col(tabs),
        ]),
    ],
    fluid=True,
    className='dbc dbc-ag-grid',
)

# -------------------------------------------------------------------------------------------------------
# * Correlation heatmap

corr_df = pd.concat([x, y], axis='columns').corr()

# Create a mask that covers the upper half of the heatmap
mask = np.triu(np.ones_like(corr_df, dtype=bool))

# Create a new correlation matrix with the upper half set to np.nan
corr_df_masked = corr_df.where(~mask, np.nan)

# where it starts
corr_heatmap_fig = px.imshow(
    corr_df_masked,
    labels=dict(x='Variable', y='Variable', color='Correlation'),
    x=corr_df.columns,
    y=corr_df.columns,
    color_continuous_scale='RdBu',
)

corr_heatmap_fig.update_layout(height=900)

corr_heatmap_container = dbc.Container(
    [html.Hr(), html.H3('Correlation Heatmap'), dcc.Graph(figure=corr_heatmap_fig)]
)


# -------------------------------------------------------------------------------------------------------
# * KDE Plot

kde_df = data[[
        'satisfaction_level',
        'last_evaluation',
        'number_project',
        'average_montly_hours',
        'time_spend_company',
]]


# ===========================================================================
# * static kde plot

plt.figure(figsize = (13,14))
plt.suptitle('Univariate Analysis - Numerical Variables - KDE Plot',fontweight = 'bold',fontsize=15,y = 1)
for i,var in enumerate(kde_df,1):
    plt.subplot(5,3,i)
    sns.kdeplot(x=var, data=kde_df, fill=True, color='r')
    plt.tight_layout()

# Get the current working directory
cwd = os.getcwd()
assets_dir = os.path.join(cwd, 'assets')
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

plot_file_path = os.path.join(assets_dir, 'kde_plot.png')
plt.savefig(plot_file_path)

# Crop the image
img = Image.open(plot_file_path)
crop_area = (0, 0, img.width, 620)
img_cropped = img.crop(crop_area)

# Add padding to top
padding = (0, 20, 0, 0)
img_padded = ImageOps.expand(img_cropped, border=padding, fill='white')
img_padded.save(plot_file_path)

# Use the relative path to the image file in an html.Img component
kde_plot_img_src = '/assets/kde_plot.png'


# ===========================================================================
# * interactive kde plot

# Create the distplots
kde_plot_figures = []
for col in kde_df.columns:
    kde_fig = ff.create_distplot([kde_df[col]], [col])
    kde_fig.update_layout(width=600, height=449, title=f'{col} Distribution')
    kde_plot_figures.append(
        dcc.Graph(figure=kde_fig, style={'border': '1px solid black', 'margin': '10px'})
    )


# ===========================================================================
# this is the one we'll use to print out the charts

kde_static_plot = dbc.Container(
    [
        html.H3('Static Plot'),
        html.Img(src=kde_plot_img_src)
    ]
)

kde_interactive_plot = dbc.Container(
    [
        html.H3('Interactive Plot'),
        html.H4('Univariate Analysis - Numerical Variables - KDE Plot'),
        html.Div(
            children=[
                kde_plot_figures[0],
                kde_plot_figures[1]
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
        html.Div(
            children=[
                kde_plot_figures[2],
                kde_plot_figures[3]
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
        html.Div(
            children=[
                kde_plot_figures[4],
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
    ]
)

kde_plot_choices = dbc.Row(
    [
        dbc.Label('Plot Type:', html_for='kde_plot_selection_form', width=1),
        dbc.Col(
            dbc.Select(
                id='kde_plot_selection_form',
                options=[
                    {'label': 'STATIC PLOT', 'value': 'static_plot'},
                    {'label': 'INTERACTIVE PLOT', 'value': 'interactable_plot'},
                ],
            ),
            width = 3,
        ),
    ],
    className ='mb-3',
)

kde_plot_selection_form = dbc.Container(
    [
        html.Hr(),
        html.H4('Select Plot Type'),
        dbc.Row([
            dbc.Col(html.P('WARNING: Interactive Plot is CPU Intensive, please use with caution.'), width=6),
            dbc.Col(
                # for interactive kde
                html.Div(
                    [
                        dbc.Badge(
                            'Click here to see why.',
                            id='component-target',
                            n_clicks=0,
                            href='#',
                            color='info',
                            className='me-1 text-decoration-none',
                        ),
                        dbc.Popover(
                            [
                                dbc.PopoverHeader('What\'s the problem with Interactive KDE Plot?'),
                                dbc.PopoverBody([
                                    html.P('The Interactive version of the KDE Plot is very computationaly expensive (CPU Intensive) because it iterates through all of the data and make each one of the variables interactable.'),
                                    html.P('This can be slow with large datasets because it involves complex math on each data point. Expect a slight delay when selecting "Interactive Plot".'),
                                    html.P('For faster loading, consider using a static KDE plot, which pre-computes the density once and displays it without needing constant recalculations.'),
                                    dbc.ListGroup(
                                            [
                                                dbc.ListGroupItem([
                                                    html.P('⚠ NOTE:'),
                                                    html.P('Avoid switching plot types while it loads.'),
                                                    ],
                                                    color='warning',
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                            target='component-target',
                            trigger='click',
                        ),
                    ],
                ),
            )
        ]),
        dbc.Form(kde_plot_choices),
    ]
)


# -------------------------------------------------------------------------------------------------------
# * Box Plot

# list of the columns to plot
box_plot_x_values = [
    'satisfaction_level',
    'last_evaluation',
    'number_project',
    'average_montly_hours',
    'time_spend_company',
]

# Create DataFrames for employees who left and Retained in the company
box_plot_left_df = data[data['left'] == 1]
box_plot_stay_df = data[data['left'] == 0]

# Create a list to store the box plot figures
box_plot_figures = []

# Create a box plot for each column in the box_plot_x_values list
for col in box_plot_x_values:
    # Create a box plot figure for the current column
    box_fig = dcc.Graph(
        figure={
            'data': [
                {'x': box_plot_stay_df[col], 'type': 'box', 'name': 'Retained'},
                {'x': box_plot_left_df[col], 'type': 'box', 'name': 'Left'},
            ],
            'layout': {
                'title': col,
                'width': 600,
                'height': 449,
            },
        },
        style={'border': '1px solid black', 'margin': '10px'},
    )

    # Add the box plot figure to the list of figures
    box_plot_figures.append(box_fig)

# this is the one we'll use to print out the charts
box_plot_container = dbc.Container(
    [
        html.Hr(),
        html.H3('Bivariate Analysis - Numerical Variables - Box Plot'),
        html.Div(
            children=[
                box_plot_figures[0],
                box_plot_figures[1],
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
        html.Div(
            children=[
                box_plot_figures[2],
                box_plot_figures[3],
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
        html.Div(
            children=[
                box_plot_figures[4],
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
    ]
)


# -------------------------------------------------------------------------------------------------------
# * AUROC graph

def train_and_predict(model, x_train, y_train, x_test):
    model.fit(x_train, y_train)
    y_score = model.predict_proba(x_test)[:, 1]
    return y_score

def add_trace(fig, fpr, tpr, auc, name):
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name=f'{name} (AUC = {auc:.3f})'))

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8)

# Train models and get predicted probabilities
y_score1 = train_and_predict(LogisticRegression(), x_train, y_train, x_test)
y_score2 = train_and_predict(DecisionTreeClassifier(), x_train, y_train, x_test)
y_score3 = train_and_predict(RandomForestClassifier(), x_train, y_train, x_test)

# Create true and false positive rates
fpr1, tpr1, _ = roc_curve(y_test, y_score1)
fpr2, tpr2, _ = roc_curve(y_test, y_score2)
fpr3, tpr3, _ = roc_curve(y_test, y_score3)

# Get AUC scores
auc1 = roc_auc_score(y_test, y_score1)
auc2 = roc_auc_score(y_test, y_score2)
auc3 = roc_auc_score(y_test, y_score3)

# Create the AUROC graph
auroc_fig = go.Figure()

# Add the ROC curve for each model
add_trace(auroc_fig, fpr1, tpr1, auc1, 'Logistic Regression')
add_trace(auroc_fig, fpr2, tpr2, auc2, 'Decision Tree')
add_trace(auroc_fig, fpr3, tpr3, auc3, 'Random Forest')

# Add the base rate line
auroc_fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Base Rate'))

# Update the layout
auroc_fig.update_layout(
    title='Area Under-Receiving Operating Characteristic Graph',
    xaxis_title='False Positive Rate',
    yaxis_title='True Positive Rate',
    autosize=False,
    width=1270,
    height=760,
)

# Create a container for the AUROC graph
auroc_container = dbc.Container(
    [html.Hr(), html.H3('AUROC Graph'), dcc.Graph(figure=auroc_fig)]
)