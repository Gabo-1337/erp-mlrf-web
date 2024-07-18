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

salary_left_total = left_company.groupby('salary')['left'].count()
salary_stay_total = stay_company.groupby('salary')['left'].count()

department_left_total = left_company.groupby('Department')['left'].count()
department_stay_total = stay_company.groupby('Department')['left'].count()

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
# * Salary and Department bar charts

bar_chart_container = dbc.Container(
    [
        html.Hr(),
        html.H3('Salary and Department Bar Charts'),
        html.Div(
            children=[
                dcc.Graph(
                    figure={
                        'data': [
                            {
                                'x': salary_stay_total.index,
                                'y': salary_stay_total.values,
                                'type': 'bar',
                                'name': 'Retained',
                            },
                            {
                                'x': salary_left_total.index,
                                'y': salary_left_total.values,
                                'type': 'bar',
                                'name': 'Left',
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
                dcc.Graph(
                    figure={
                        'data': [
                            {
                                'x': department_stay_total.index,
                                'y': department_stay_total.values,
                                'type': 'bar',
                                'name': 'Retained',
                            },
                            {
                                'x': department_left_total.index,
                                'y': department_left_total.values,
                                'type': 'bar',
                                'name': 'Left',
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
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
            },
        ),
    ]
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

kde_df = data[
    [
        'satisfaction_level',
        'last_evaluation',
        'number_project',
        'average_montly_hours',
        'time_spend_company',
    ]
]


# ===========================================================================
# * static plot

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
# * interactive plot

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
                            href="#",
                            color="info",
                            className="me-1 text-decoration-none",
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