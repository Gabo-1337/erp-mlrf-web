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
from sklearn.metrics import confusion_matrix

# Third-party imports for machine learning models; used for AUROC Curve
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

# Third-party imports for web application
from dash import dcc, html
import dash_bootstrap_components as dbc

# local imports
import bpred as bd


# -------------------------------------------------------------------------------------------------------
# * initialization

# * dataset initalization
data = pd.read_csv('https://raw.githubusercontent.com/CS-DREAM-TEAM/assets/main/ibm_hr_processed.csv')

df_visuals = data.copy()

# * variable initializations
left_company = df_visuals[df_visuals['Attrition_Yes'] == 1]
stay_company = df_visuals[df_visuals['Attrition_Yes'] == 0]

x = df_visuals[bd.universal_features]
y = df_visuals[bd.universal_target]

# x = inputs
# y = target

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
# df_visuals = df_preprocess

# ===========================================================================
# * TAB 1 Environment Satisfaction bar plot

env_satisfaction_bins = [1, 2, 3, 4, 5]
env_satisfaction_labels = ['Low', 'Medium', 'High', 'Very High']

df_visuals['env_satisfaction_Group'] = pd.cut(df_visuals['EnvironmentSatisfaction'], bins=env_satisfaction_bins, labels=env_satisfaction_labels, right=False)
env_satisfaction_grouped_df = df_visuals.groupby(['env_satisfaction_Group', 'Attrition_Yes'], observed=True).size().unstack(fill_value=0)

# Create the bar chart
env_satis_trace_stay = go.Bar(x=env_satisfaction_grouped_df.index, y=env_satisfaction_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
env_satis_trace_left = go.Bar(x=env_satisfaction_grouped_df.index, y=env_satisfaction_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

satis_layout = go.Layout(
    title='Employee status by Environment Satisfaction Level',
    xaxis=dict(title='Environment Satisfaction Level'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

env_satisfaction_bins_fig = go.Figure(data=[env_satis_trace_stay, env_satis_trace_left], layout=satis_layout)

env_satisfaction_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=env_satisfaction_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Employment Status by Environment Satisfaction')),
                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.P("This chart visualizes the relationship between employee satisfaction with their work environment and their decision to stay or leave the company."),
                    html.Ul([
                        html.Li([
                            html.Strong('X-Axis:'),
                            html.Ul([
                                html.Li('The x-axis categorizes employees based on their reported satisfaction with their work environment, ranging from "Low" to "Very High."'),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Y-Axis:'),
                            html.Ul([
                                html.Li('The y-axis represents the number of employees in each satisfaction category.'),
                            ])
                        ]),
                    ]),
                    html.H5(html.Strong('Employee Status and Environment Satisfaction:')),
                    html.Ul([
                        html.Li([
                            html.Strong('Low - Medium:'),
                            html.Ul([
                                html.Li('The bar chart interprets that the employee count of environment satisfaction for the Low - Medium range has less employees staying and has more leaving the company than the other range.'),
                            ])
                        ]),
                        
                        html.Li([
                            html.Strong('High - Very High:'),
                            html.Ul([
                                html.Li('The bar chart interprets that the employee count of environment satisfaction for the High - Very High range has more employees staying and a steady rate of employees leaving the company.'),
                            ])
                        ]),
                    ]),
                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li('While there are some employees who left despite reporting high or very high satisfaction levels, the overall trend suggests that a positive work environment is generally associated with higher retention rates.'),
                        html.Li('This chart provides evidence that employee satisfaction with their work environment is a significant factor in determining whether they will stay or leave a company.'),
                        html.Li('Organizations that prioritize creating a positive and satisfying work environment are more likely to retain their employees.'),
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
# * TAB 2 job_involvement_chart_container bar plot

job_involvement_bins = [1, 2, 3, 4, 5]
job_involvement_labels = ['Low', 'Medium', 'High', 'Very High']

df_visuals['job_involvement_Group'] = pd.cut(df_visuals['JobInvolvement'], bins=job_involvement_bins, labels=job_involvement_labels, right=False)
job_involv_grouped_df = df_visuals.groupby(['job_involvement_Group', 'Attrition_Yes'], observed=True).size().unstack(fill_value=0)
# Create the bar chart
job_involv_trace_stay = go.Bar(x=job_involv_grouped_df.index, y=job_involv_grouped_df[0], name='Retained(No)', marker_color='#1f77b4') # blue
job_involv_trace_left = go.Bar(x=job_involv_grouped_df.index, y=job_involv_grouped_df[1], name='Left(Yes)', marker_color='#ff7f0e') # orange

job_involv_layout = go.Layout(
    title='Employee status by Job Involvement',
    xaxis=dict(title='Job Involvement'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

job_involvement_bins_fig = go.Figure(data=[job_involv_trace_stay, job_involv_trace_left], layout=job_involv_layout)

job_involvement_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=job_involvement_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Job Involvement')),
                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.P("This chart visualizes the involvement of employees with their job and their decision to stay or leave the company."),
                    html.H5(html.Strong('Employee Status and Job Involvement:')),
                    html.Ul([
                        html.Li([
                            html.Strong('Low:'),
                            html.Ul([
                                html.Li("Employees in this category have a minimal sense of involvement in their jobs. They may feel disconnected from their work or lack a strong sense of purpose."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Medium:'),
                            html.Ul([
                                html.Li("Employees in this category have a moderate level of job involvement. They may feel somewhat connected to their work but may not be fully invested or enthusiastic."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('High:'),
                            html.Ul([
                                html.Li("Employees in this category have a strong sense of involvement in their jobs. They identify with their work and find it personally meaningful.")
                            ])
                        ]),
                        html.Li([
                            html.Strong('Very High:'),
                            html.Ul([
                                html.Li("Employees in this category have an extremely high level of job involvement. They are deeply committed to their work and find it highly fulfilling.")
                            ])
                        ])
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li("The chart provides evidence that employee job involvement is a significant factor in determining whether they will stay or leave a company."),
                        html.Li("Organizations that can foster a work environment that promotes high job involvement are more likely to retain their employees.")
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
# * TAB 3 overtime_chart_container plot

overtime_bins = [0, 1, 2]
overtime_labels = ['Yes', 'No']

df_visuals['overtime_Group'] = pd.cut(df_visuals['OverTime_Yes'], bins=overtime_bins, labels=overtime_labels, right=False)
number_project_grouped_df = df_visuals.groupby(['overtime_Group', 'Attrition_Yes'], observed=True).size().unstack(fill_value=0)

overtime_trace_stay = go.Bar(x=number_project_grouped_df.index, y=number_project_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
overtime_trace_left = go.Bar(x=number_project_grouped_df.index, y=number_project_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

overtime_layout = go.Layout(
    title='Employee status by Overtime',
    xaxis=dict(title='Overtime'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

overtime_bins_fig = go.Figure(data=[overtime_trace_stay, overtime_trace_left], layout=overtime_layout)

overtime_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=overtime_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.Div([
                        html.H4(html.Strong('Explanation: Employment Status by Overtime')),
                        html.P("This chart visualizes employees who have overtime privileges and their decision to stay or leave the company."),

                        html.H5(html.Strong('Bar Chart Interpretation:')),
                        html.Ul([
                            html.Li([
                                html.Strong('Yes:'),
                                html.Ul([
                                    html.Li("Employees that have paid overtime are more likely to stay at their respective company."),
                                ])
                            ]),
                            html.Li([
                                html.Strong('No:'),
                                html.Ul([
                                    html.Li("Employees that does not have paid overtime are more likely to leave their current company."),
                                ])
                            ])
                        ]),

                        html.H5(html.Strong('Conclusion:')),
                        html.Ul([
                            html.Li("The chart interprets that employees who have overtime privileges are more likely to stay with the company compared to those who do not."),
                            ]),
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
# # * TAB 4 perf_rating_chart_container

perf_rating_bins = [1, 2, 3, 4, 5]
perf_rating_labels = ['Low', 'Good', 'Excellent', 'Outstanding']

df_visuals['perf_rating_Group'] = pd.cut(df_visuals['PerformanceRating'], bins=perf_rating_bins, labels=perf_rating_labels, right=False)
perf_rating_df = df_visuals.groupby(['perf_rating_Group', 'Attrition_Yes'], observed=True).size().unstack(fill_value=0)

perf_rating_trace_stay = go.Bar(x=perf_rating_df.index, y=perf_rating_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
perf_rating_trace_left = go.Bar(x=perf_rating_df.index, y=perf_rating_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

perf_rating_layout = go.Layout(
    title='Employee status by Performance Rating',
    xaxis=dict(title='Performance Rating'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

perf_rating_bins_fig = go.Figure(data=[perf_rating_trace_stay, perf_rating_trace_left], layout=perf_rating_layout)

perf_rating_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=perf_rating_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Performance Rating')),
                    html.P("This chart visualizes the relationship between employee performance ratings and their decision to stay or leave the company."),

                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('Excellent:'),
                            html.Ul([
                                html.Li("A significantly higher number of employees rated as excellent performers remained with the company."),
                                html.Li("This suggests a strong correlation between high performance ratings and employee retention."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Outstanding:'),
                            html.Ul([
                                html.Li("While there are some employees who left despite being rated as excellent performers, the overall trend indicates that outstanding performance is a significant factor in employee retention."),
                            ])
                        ]),
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li("The chart interprets employees who are rated as excellent or outstanding performers are more likely to stay with the company compared to those with lower performance ratings."),
                        html.Li("This suggests that recognizing and rewarding high performance can be an effective strategy for retaining top talent."),
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
# * TAB 5 relation_satisfaction_chart_container

relation_satisfaction_bins = [1, 2, 3, 4, 5]
relation_satisfaction_labels = ['Low', 'Medium', 'High', 'Very High']

df_visuals['relation_satisfaction_Group'] = pd.cut(df_visuals['RelationshipSatisfaction'], bins=relation_satisfaction_bins, labels=relation_satisfaction_labels, right=False)
relation_satisfaction_grouped_df = df_visuals.groupby(['relation_satisfaction_Group', 'Attrition_Yes'], observed=True).size().unstack(fill_value=0)

relation_satisfaction_trace_stay = go.Bar(x=relation_satisfaction_grouped_df.index, y=relation_satisfaction_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
relation_satisfaction_trace_left = go.Bar(x=relation_satisfaction_grouped_df.index, y=relation_satisfaction_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

relation_satisfaction_layout = go.Layout(
    title='Employee status by Relationship Satisfaction',
    xaxis=dict(title='Relationship Satisfaction'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

relation_satisfaction_bins_fig = go.Figure(data=[relation_satisfaction_trace_stay, relation_satisfaction_trace_left], layout=relation_satisfaction_layout)

relation_satisfaction_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=relation_satisfaction_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Relationship Satisfaction')),
                    html.P("This chart visualizes the relationship between employee relationship satisfaction and their decision to stay or leave the company."),

                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('Low:'),
                            html.Ul([
                                html.Li("Employees in this category have a negative or minimal level of satisfaction with their relationships."),
                                html.Li("They may experience conflicts, misunderstandings, or a lack of support."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Medium:'),
                            html.Ul([
                                html.Li("Employees in this category have a moderate level of relationship satisfaction."),
                                html.Li("They may have some positive interactions but also experience challenges or tensions."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('High:'),
                            html.Ul([
                                html.Li("Employees in this category have a strong sense of satisfaction with their relationships."),
                                html.Li("They feel supported, valued, and respected by others."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Very High:'),
                            html.Ul([
                                html.Li("Employees in this category have an exceptionally high level of relationship satisfaction."),
                                html.Li("They have strong, positive bonds with their colleagues and superiors, and feel highly connected to the workplace community."),
                            ])
                        ]),
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li("The chart interprets that employees who have strong relationships with their colleagues and superiors are more likely to stay with the company compared to those with lower relationship satisfaction."),
                        html.Li("This variable is crucial in understanding how an employee's interpersonal connections can impact their overall job satisfaction and, ultimately, their decision to stay or leave a company."),
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
# # * TAB 6 job_satisfaction_chart_container

job_satisfaction_bins = [1, 2, 3, 4, 5]
job_satisfaction_labels = ['Low', 'Medium', 'High', 'Very High']

df_visuals['job_satisfaction_Group'] = pd.cut(df_visuals['JobSatisfaction'], bins=job_satisfaction_bins, labels=job_satisfaction_labels, right=False)
job_satisfaction_grouped_df = df_visuals.groupby(['job_satisfaction_Group', 'Attrition_Yes'], observed=True).size().unstack(fill_value=0)

job_satisfaction_trace_stay = go.Bar(x=job_satisfaction_grouped_df.index, y=job_satisfaction_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
job_satisfaction_trace_left = go.Bar(x=job_satisfaction_grouped_df.index, y=job_satisfaction_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

job_satisfaction_layout = go.Layout(
    title='Employee status by Job Satisfaction',
    xaxis=dict(title='Job Satisfaction'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

job_satisfaction_bins_fig = go.Figure(data=[job_satisfaction_trace_stay, job_satisfaction_trace_left], layout=job_satisfaction_layout)

job_satisfaction_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=job_satisfaction_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Job Satisfaction')),
                    html.P("This chart visualizes the relationship between employee job satisfaction and their decision to stay or leave the company."),

                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('Low:'),
                            html.Ul([
                                html.Li("Employees in this category have a negative or minimal level of job satisfaction."),
                                html.Li("They may find their work unfulfilling, challenging, or stressful."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Medium:'),
                            html.Ul([
                                html.Li("Employees in this category have a moderate level of job satisfaction."),
                                html.Li("They may have some positive aspects to their jobs but also experience dissatisfaction or frustration."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('High:'),
                            html.Ul([
                                html.Li("Employees in this category have a strong sense of job satisfaction."),
                                html.Li("They find their work meaningful, challenging, and rewarding."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Very High:'),
                            html.Ul([
                                html.Li("Employees in this category have an exceptionally high level of job satisfaction."),
                                html.Li("They are deeply engaged in their work and derive great fulfillment from it."),
                            ])
                        ]),
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li("The chart interprets that employees who are highly satisfied with their jobs are more likely to stay with the company compared to those with lower job satisfaction."),
                        html.Li("This variable is crucial in understanding how an employee's overall feelings about their work can impact their decision to stay or leave a company."),
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
# * TAB 7 job_level_chart_container bar plot

job_level_bins = [1, 2, 3, 4, 5, 6]
job_level_labels = ['Entry', 'Intermediate', 'Experienced', 'Advanced', 'Expert']

df_visuals['job_level_Group'] = pd.cut(df_visuals['JobLevel'], bins=job_level_bins, labels=job_level_labels, right=False)
job_level_grouped_df = df_visuals.groupby(['job_level_Group', 'Attrition_Yes'], observed=True).size().unstack(fill_value=0)

job_level_trace_stay = go.Bar(x=job_level_grouped_df.index, y=job_level_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
job_level_trace_left = go.Bar(x=job_level_grouped_df.index, y=job_level_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

job_level_layout = go.Layout(
    title='Employee status by Job Level',
    xaxis=dict(title='Job Level'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

job_level_bins_fig = go.Figure(data=[job_level_trace_stay, job_level_trace_left], layout=job_level_layout)

job_level_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=job_level_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Job Level')),
                    html.P("This chart visualizes the relationship between employee job level and their decision to stay or leave the company."),

                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('Entry Level:'),
                            html.Ul([
                                html.Li("Employees at this level are typically new to the organization or have limited experience."),
                                html.Li("They may be in entry-level positions or internships."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Intermediate Level:'),
                            html.Ul([
                                html.Li("Employees at this level have some experience and are typically responsible for carrying out routine tasks and assignments."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Experienced Level:'),
                            html.Ul([
                                html.Li("Employees at this level have a significant amount of experience and are often responsible for more complex tasks and projects."),
                                html.Li("They may also have supervisory responsibilities."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Advanced:'),
                            html.Ul([
                                html.Li("Employees at this level have advanced skills and expertise in their field."),
                                html.Li("They often hold leadership positions or are subject matter experts."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Expert:'),
                            html.Ul([
                                html.Li("Employees at this level are considered to be highly skilled and knowledgeable in their field."),
                                html.Li("They may be recognized as industry experts or thought leaders."),
                            ])
                        ]),
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li("The chart interprets that employees at higher job levels are more likely to stay with the company compared to those at lower levels."),
                        html.Li("This variable is crucial in understanding how an employee's position within the organization can impact their job satisfaction, opportunities for advancement, and ultimately, their decision to stay or leave the company."),
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
# * TAB 8 wl_balance_chart_container bar plot

wl_balance_bins = [1, 2, 3, 4, 5]
wl_balance_labels = ['Bad', 'Good', 'Better', 'Best']

df_visuals['wl_balance_Group'] = pd.cut(df_visuals['WorkLifeBalance'], bins=wl_balance_bins, labels=wl_balance_labels, right=False)
wl_balance_grouped_df = df_visuals.groupby(['wl_balance_Group', 'Attrition_Yes'], observed=True).size().unstack(fill_value=0)

wl_balance_trace_stay = go.Bar(x=wl_balance_grouped_df.index, y=wl_balance_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
wl_balance_trace_left = go.Bar(x=wl_balance_grouped_df.index, y=wl_balance_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

wl_balance_layout = go.Layout(
    title='Employee status by Work-Life Balance',
    xaxis=dict(title='Work-Life Balance'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

wl_balance_bins_fig = go.Figure(data=[wl_balance_trace_stay, wl_balance_trace_left], layout=wl_balance_layout)

wl_balance_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=wl_balance_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Work-Life Balance')),
                    html.P("This chart visualizes the relationship between employee work-life balance and their decision to stay or leave the company."),

                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('Bad:'),
                            html.Ul([
                                html.Li("Employees in this category have a poor work-life balance."),
                                html.Li("They may be overwhelmed by work demands, have difficulty managing their time, or struggle to balance their professional and personal commitments."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Good:'),
                            html.Ul([
                                html.Li("Employees in this category have a decent work-life balance."),
                                html.Li("They are able to manage their work and personal responsibilities to some extent, but may still experience occasional challenges."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Better:'),
                            html.Ul([
                                html.Li("Employees in this category have a good work-life balance."),
                                html.Li("They are able to effectively manage their time and priorities, and maintain a healthy balance between work and personal life."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Best:'),
                            html.Ul([
                                html.Li("Employees in this category have an excellent work-life balance."),
                                html.Li("They are highly skilled at managing their time and priorities, and consistently achieve a positive balance between work and personal life."),
                            ])
                        ]),
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li("The chart interprets that employees at higher job levels are more likely to stay with the company compared to those at lower levels."),
                        html.Li("This variable is crucial in understanding how an employee's position within the organization can impact their job satisfaction, opportunities for advancement, and ultimately, their decision to stay or leave the company."),
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
# * TAB 9 yrs_lastpromote_chart_container bar plot

yrs_lastpromote_bins = [1, 4, 7, 10, 13, 15]
yrs_lastpromote_labels = ['1 - 3', '3 - 6', '6 - 9', '9 - 12', '12 - 15']

df_visuals['yrs_lastpromote_Group'] = pd.cut(df_visuals['YearsSinceLastPromotion'], bins=yrs_lastpromote_bins, labels=yrs_lastpromote_labels, right=False)
yrs_lastpromote_grouped_df = df_visuals.groupby(['yrs_lastpromote_Group', 'Attrition_Yes'], observed=True).size().unstack(fill_value=0)

yrs_lastpromote_trace_stay = go.Bar(x=yrs_lastpromote_grouped_df.index, y=yrs_lastpromote_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
yrs_lastpromote_trace_left = go.Bar(x=yrs_lastpromote_grouped_df.index, y=yrs_lastpromote_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

yrs_lastpromote_layout = go.Layout(
    title='Employee status by Years Since Last Promotion',
    xaxis=dict(title='Years Since Last Promotion'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

yrs_lastpromote_bins_fig = go.Figure(data=[yrs_lastpromote_trace_stay, yrs_lastpromote_trace_left], layout=yrs_lastpromote_layout)

yrs_lastpromote_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=yrs_lastpromote_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Years Since Last Promotion')),
                    html.P("This chart visualizes the relationship between the number of years since an employee's last promotion and their decision to stay or leave the company."),

                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('1 - 3:'),
                            html.Ul([
                                html.Li("Employees in this category have been promoted within the past 1-3 years."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('3 - 6:'),
                            html.Ul([
                                html.Li("Employees in this category have been promoted between 3 and 6 years ago."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('6 - 9:'),
                            html.Ul([
                                html.Li("Employees in this category have been promoted between 6 and 9 years ago."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('9 - 12:'),
                            html.Ul([
                                html.Li("Employees in this category have been promoted between 9 and 12 years ago."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('12 - 15:'),
                            html.Ul([
                                html.Li("Employees in this category have been promoted between 12 and 15 years ago."),
                            ])
                        ])
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li("The chart interprets that employees who are promoted recently are more likely to stay with the company compared to those who have not been promoted in a longer period."),
                        html.Li("This variable is crucial in understanding how an employee's career progression can impact their job satisfaction, motivation, and ultimately, their decision to stay or leave the company."),
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
# * TAB 10 monthly_income_chart_container bar plot

monthly_income_bins = [1009, 2911, 4919, 8379, 19999]
monthly_income_labels = ['0 - 25%', '25% - 50%', '50% - 75%', '75% - 100%']

df_visuals['monthly_income_Group'] = pd.cut(df_visuals['MonthlyIncome'], bins=monthly_income_bins, labels=monthly_income_labels, right=False)
monthly_income_grouped_df = df_visuals.groupby(['monthly_income_Group', 'Attrition_Yes'], observed=True).size().unstack(fill_value=0)

monthly_income_trace_stay = go.Bar(x=monthly_income_grouped_df.index, y=monthly_income_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
monthly_income_trace_left = go.Bar(x=monthly_income_grouped_df.index, y=monthly_income_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

monthly_income_layout = go.Layout(
    title='Employee status by Monthly Income',
    xaxis=dict(title='Monthly Income'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

monthly_income_bins_fig = go.Figure(data=[monthly_income_trace_stay, monthly_income_trace_left], layout=monthly_income_layout)

monthly_income_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=monthly_income_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Monthly Income')),
                    html.P("This chart visualizes the relationship between employee monthly income and their decision to stay or leave the company."),

                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('0 - 25%:'),
                            html.Ul([
                                html.Li("Employees in this category have a monthly income that falls within the lowest 25% of the salary distribution in the organization or industry."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('25% - 50%:'),
                            html.Ul([
                                html.Li("Employees in this category have a monthly income that falls within the second quartile of the salary distribution."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('50% - 75%:'),
                            html.Ul([
                                html.Li("Employees in this category have a monthly income that falls within the third quartile of the salary distribution."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('75% - 100%:'),
                            html.Ul([
                                html.Li("Employees in this category have a monthly income that falls within the highest 25% of the salary distribution in the organization or industry."),
                            ])
                        ])
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li("The chart interprets that The highest number of employees who left were in the 25-50% income quartile."),
                        html.Li("However, this may not be a conclusive indicator of income as a primary factor in employee turnover, as other factors could be influencing the decision."),
                        html.Li("This variable is crucial in understanding how an employee's financial compensation can impact their job satisfaction, motivation, and ultimately, their decision to stay or leave a company."),
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
# * TAB 11 gen_group_chart_container bar plot

age_bins = [18, 30, 50, 99]
age_labels = ['Young_Adults', 'Adults', 'Near_Retirement']

df_visuals['vis_Age_group'] = pd.cut(df_visuals['Age'], bins=age_bins, labels=age_labels, right=False)
age_group_grouped_df = df_visuals.groupby(['vis_Age_group', 'Attrition_Yes'], observed=True).size().unstack(fill_value=0)

age_group_trace_stay = go.Bar(x=age_group_grouped_df.index, y=age_group_grouped_df[0], name='Retained(0)', marker_color='#1f77b4') # blue
age_group_trace_left = go.Bar(x=age_group_grouped_df.index, y=age_group_grouped_df[1], name='Left(1)', marker_color='#ff7f0e') # orange

gen_group_layout = go.Layout(
    title='Employee status by Age Group',
    xaxis=dict(title='Age Group'),
    yaxis=dict(title='Count'),
    barmode='group',
    width= 600,
    height= 449,
)

age_group_bins_fig = go.Figure(data=[age_group_trace_stay, age_group_trace_left], layout=gen_group_layout)

gen_group_chart_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(figure=age_group_bins_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Employment Status by Age Groups')),
                    html.P("This chart visualizes the relationship between employee age groups and their decision to stay or leave the company."),

                    html.H5(html.Strong('Bar Chart Interpretation:')),
                    html.Ul([
                        html.Li([
                            html.Strong('Young Adults:'),
                            html.Ul([
                                html.Li("Typically refers to employees in their early to mid-20s."),
                                html.Li("This group is often characterized by their energy, enthusiasm, and desire for growth and development."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Adults:'),
                            html.Ul([
                                html.Li("Typically refers to employees in their late 30s to early 60s. "),
                                html.Li("This group is often characterized by their established careers, greater experience, and increased responsibilities."),
                            ])
                        ]),
                        html.Li([
                            html.Strong('Near Retirement:'),
                            html.Ul([
                                html.Li("Typically refers to employees in their late 60s to retirement age. "),
                                html.Li("This group is often characterized by their accumulated experience, knowledge, and preparation for retirement."),
                            ])
                        ])
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.Ul([
                        html.Li("The chart interprets that age can be a factor in employee retention, with Adults demonstrating a higher likelihood to stay."),
                        html.Li("The chart represents the different age groups within the organization, which can influence employee expectations, motivations, and career goals."),
                        html.Li("Understanding these age-related factors can be helpful in developing retention strategies that cater to the specific needs and preferences of each group."),
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

# ===========================================================================
# ! BAR CHART TABS

tab1 = dbc.Tab(env_satisfaction_chart_container, label='Environment Satisfaction')
tab2 = dbc.Tab(job_involvement_chart_container, label='Job Involvement')
tab3 = dbc.Tab(overtime_chart_container, label='Overtime')
tab4 = dbc.Tab(perf_rating_chart_container, label='Performance Rating')
tab5 = dbc.Tab(relation_satisfaction_chart_container, label='Relationship Satisfaction')
tab6 = dbc.Tab(job_satisfaction_chart_container, label='Job Satisfaction')
tab7 = dbc.Tab(job_level_chart_container, label='Job Level')
tab8 = dbc.Tab(wl_balance_chart_container, label='Work-Life Balance')
tab9 = dbc.Tab(yrs_lastpromote_chart_container, label='Years Since Last Promotion')
tab10 = dbc.Tab(monthly_income_chart_container, label='Monthly Income')
tab11 = dbc.Tab(gen_group_chart_container, label='Age Group')

tabs = dbc.Card(dbc.Tabs([tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11]))

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
    [html.Hr(), html.H3('Correlation Heatmap'), dcc.Graph(figure=corr_heatmap_fig, style={'border': '1px solid black', 'margin': '10px'})]
)

# -------------------------------------------------------------------------------------------------------
# * Confusion Matrix

# For confusion matrix only
x_cf_train, x_cf_test, y_cf_train, y_cf_test = train_test_split(x, y, train_size=0.01)

# Confusion matrix
cfm_y_predicted = bd.loaded_rf_model.predict(x_cf_test)
cm = confusion_matrix(y_cf_test, cfm_y_predicted)

# Convert the confusion matrix to a DataFrame for easier plotting
cm_df = pd.DataFrame(cm)

# Create a confusion matrix figure using Plotly Express
cfm_fig = px.imshow(
    cm_df,
    labels=dict(x='Predicted', y='True', color='Count'),
    x=[f'Predicted {label}' for label in bd.loaded_rf_model.classes_],
    y=[f'True {label}' for label in bd.loaded_rf_model.classes_],
    color_continuous_scale='RdBu',
)

true_negatives = cm_df.iloc[0, 0]
false_positives = cm_df.iloc[0, 1]
false_negatives = cm_df.iloc[1, 0]
true_positives = cm_df.iloc[1, 1]
total_correct = true_negatives + true_positives
total_wrong = false_positives + false_negatives

tn_text = f"The top left cell represents True Negatives (TN) with a count of {true_negatives}. This means that our model correctly predicted {true_negatives} instances where the actual and predicted values were both 0."
fp_text = f"The top right cell represents False Positives (FP) with a count of {false_positives}. This means that there were {false_positives} instances where our model incorrectly predicted a value of 1 when the actual value was 0."
fn_text = f"The bottom left cell represents False Negatives (FN) with a count of {false_negatives}. This means that there were {false_negatives} instances where our model incorrectly predicted a value of 0 when the actual value was 1."
tp_text = f"The bottom right cell represents True Positives (TP) with a count of {true_positives}. This means that our model correctly predicted {true_positives} instances where the actual and predicted values were both 1."
conclusion_text = f"So, out of a total of {len(y_cf_test)} instances in our test set (y_test), our model made {total_correct} correct predictions (TN + TP) and only {total_wrong} incorrect predictions (FP + FN). This indicates that our model has a high accuracy rate."


# Add annotations (the count) to each cell
annotations = []
for i, row in enumerate(cm):
    for j, value in enumerate(row):
        annotations.append(
            dict(
                x=j,
                y=i,
                text=str(value),
                font=dict(color='white'),
                showarrow=False
            )
        )

cfm_fig.update_layout(width= 600,
                      height= 449,
                      annotations=annotations)

cfm_container = dbc.Container(
    [
        html.Hr(),
        html.Div(
            children=[
                dcc.Graph(figure=cfm_fig, style={'border': '1px solid black', 'margin': '10px'}),
                html.Div([
                    html.H4(html.Strong('Explanation: Confusion Matrix')),
                    html.P("A confusion matrix is a table that is often used to describe the performance of a classification model on a set of data for which the true values are known. It's a way to visualize the performance of our model, and it's especially useful for multi-class classification problems."),

                    html.H5(html.Strong('Chart Interpretation:')),
                    html.Ul([
                        html.Li(tn_text),
                        html.Li(fp_text),
                        html.Li(fn_text),
                        html.Li(tp_text),
                    ]),

                    html.H5(html.Strong('Conclusion:')),
                    html.P(conclusion_text),
                ])
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
    ],
)

# -------------------------------------------------------------------------------------------------------
# * KDE Plot

kde_df = df_visuals[bd.universal_all_variable]

# ===========================================================================
# # * static kde plot

plt.figure(figsize = (12,17))
plt.suptitle('Univariate Analysis - Numerical Variables - KDE Plot',fontweight = 'bold',fontsize=15,y = 1)
for i,var in enumerate(kde_df,1):
    plt.subplot(8,4,i)
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
crop_area = (0, 0, img.width, 1000)
img_cropped = img.crop(crop_area)

# Add padding to top
padding = (0, 20, 0, 0)
img_padded = ImageOps.expand(img_cropped, border=padding, fill='white')
img_padded.save(plot_file_path)

# Use the relative path to the image file in an html.Img component
kde_plot_img_src = '/assets/kde_plot.png'

# ===========================================================================
# this is the one we'll use to print out the charts

kde_plot_container = dbc.Container(
    [
        html.Hr(),
        html.H3('Univariate Analysis - KDE Plot'),
        html.Img(src=kde_plot_img_src, style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'})
    ]
)

# -------------------------------------------------------------------------------------------------------
# * Box Plot

# list of the columns to plot
box_plot_values = df_visuals[bd.universal_all_variable]

plt.figure(figsize = (12,17))
plt.suptitle('Bivariate Analysis - Numerical Variables - Box Plot',fontweight = 'bold',fontsize=15,y = 1)
for i, var in enumerate(box_plot_values, 1):
    plt.subplot(8, 4, i) #(8 rows, 4 columns)
    sns.boxplot(data=box_plot_values, x="Attrition_Yes", y=var, hue="Attrition_Yes",
                palette=['tab:blue', 'tab:orange'], fill=False, gap=.1)
    plt.legend(fontsize=7, loc='center')
    plt.tight_layout()

# Get the current working directory
cwd = os.getcwd()
assets_dir = os.path.join(cwd, 'assets')
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

plot_file_path = os.path.join(assets_dir, 'box_plot.png')
plt.savefig(plot_file_path)

# Crop the image
img = Image.open(plot_file_path)
crop_area = (0, 0, img.width, 1000)
img_cropped = img.crop(crop_area)

# Add padding to top
padding = (0, 20, 0, 0)
img_padded = ImageOps.expand(img_cropped, border=padding, fill='white')
img_padded.save(plot_file_path)

# Use the relative path to the image file in an html.Img component
box_plot_img_src = '/assets/box_plot.png'


# * Violin Plot

violin_plot_values = df_visuals[bd.universal_all_variable]

# Create the figure for the violin plots
plt.figure(figsize=(12, 17))
plt.suptitle('Bivariate Analysis - Numerical Variables - Violin Plot', fontweight='bold', fontsize=15, y=1)

# Generate the violin plots
for i, var in enumerate(violin_plot_values, 1):
    plt.subplot(8, 4, i)  # (8 rows, 4 columns)
    sns.violinplot(data=violin_plot_values, x="Attrition_Yes", y=var, hue="Attrition_Yes",
                   palette=['tab:blue', 'tab:orange'], split=True)
    plt.legend(fontsize=7, loc='upper right')
    plt.tight_layout()

# Get the current working directory
cwd = os.getcwd()
assets_dir = os.path.join(cwd, 'assets')
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

# Save the plot as an image
plot_file_path = os.path.join(assets_dir, 'violin_plot.png')
plt.savefig(plot_file_path)

# Crop the image
img = Image.open(plot_file_path)
crop_area = (0, 0, img.width, 1000)
img_cropped = img.crop(crop_area)

# Add padding to top
padding = (0, 20, 0, 0)
img_padded = ImageOps.expand(img_cropped, border=padding, fill='white')
img_padded.save(plot_file_path)

# Use the relative path to the image file in an html.Img component
violin_plot_img_src = '/assets/violin_plot.png'

# ===========================================================================
# this is the one we'll use to print out the charts

box_plot_container = dbc.Container(
    [
        html.Hr(),
        html.H3('Bivariate Analysis - Box Plot'),
        html.Img(src=box_plot_img_src, style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),
        html.Hr(),
        html.H3('Bivariate Analysis - Violin Plot'),
        html.Img(src=violin_plot_img_src, style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'})
    ]
)



# # -------------------------------------------------------------------------------------------------------
# # * AUROC graph

def add_trace(fig, fpr, tpr, auc, name):
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name=f'{name} (AUC = {auc:.3f})'))

def evaluate_models(models, x_train, y_train, x_test, y_test):
    results = {}
    for name, model in models.items():
        model.fit(x_train, y_train)
        if hasattr(model, "predict_proba"):
            y_score = model.predict_proba(x_test)[:, 1]
        else:
            y_score = model.decision_function(x_test)
        fpr, tpr, _ = roc_curve(y_test, y_score)
        auc = roc_auc_score(y_test, y_score)
        results[name] = (fpr, tpr, auc)
        print(f'{name} model AUC: {auc:.3f}')
    return results


x_dfvs_train, x_dfvs_test, y_dfvs_train, y_dfvs_test = train_test_split(x, y, train_size=0.8)

# Define models, excluding Random Forest since it's pre-trained
models = {
    'Decision Tree': DecisionTreeClassifier(),
    'KNN': KNeighborsClassifier(),
    'SVC': SVC(probability=True),
    'MLP': MLPClassifier(),
    'LDA': LinearDiscriminantAnalysis()
}

# Evaluate models
results = evaluate_models(models, x_dfvs_train, y_dfvs_train, x_dfvs_test, y_dfvs_test)

# Add the pre-trained Random Forest model to the results
rf_y_score = bd.loaded_rf_model.predict_proba(x_dfvs_test)[:, 1]
fpr_rf, tpr_rf, _ = roc_curve(y_dfvs_test, rf_y_score)
auc_rf = roc_auc_score(y_dfvs_test, rf_y_score)
results['Random Forest'] = (fpr_rf, tpr_rf, auc_rf)
print(f'Random Forest model AUC: {auc_rf:.3f}')

# Create the AUROC graph
auroc_fig = go.Figure()

# Add the ROC curve for each model
for name, (fpr, tpr, auc) in results.items():
    add_trace(auroc_fig, fpr, tpr, auc, name)

# Add the base rate line
auroc_fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Base Rate'))

# Update the layout
auroc_fig.update_layout(
    title='Area Under Receiver Operating Characteristic (ROC) Curve',
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