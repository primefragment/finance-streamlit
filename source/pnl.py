import dash
from dash import dcc, html
import dash.dependencies as dd
import pandas as pd
import plotly.express as px
from pathlib import Path

# Load your CSV file into a DataFrame
current_dir = Path(__file__).parent
root_dir = current_dir.parent
df = pd.read_csv(root_dir / 'data' / 'daily_journal_rrsp_usd.csv')


# Figures
fig1=px.line(df, x='Date', y='Wakeup Time', title='Wakeup Time', line_shape='spline', range_y=[4,10], width=300)
fig1.update_layout(xaxis = dict(tickformat='%d-%b\n%a', title_text = ''), yaxis = dict(title_text = '', tickmode='linear'))

fig2=px.line(df, x='Date', y=['Hours Planned','Total Work'], title='Hours Planned/Worked', range_y=[0,9], line_shape='spline', width=300)
fig2.update_layout(legend_title='', xaxis = dict(tickformat='%d-%b\n%a', title_text = ''), yaxis = dict(tickmode='linear',title_text = ''))

fig3=px.bar(df, x='Date', y=['GameDev','Growth','Finance','Venture'], title='Work Breakdown', width=300)
fig3.update_layout(legend_title='', bargap=0.5, xaxis= dict(tickformat='%d-%b\n%a', tickmode='array', tickvals=df['Date'], title_text = ''), yaxis = dict(title_text = ''))


# App and Layout
# Initialize the Dash app
app = dash.Dash(__name__)

# Create your layout
app.layout = html.Div([
    dcc.Graph(
        id='graph1',
        figure=fig1
    ),
    dcc.Graph(
        id='graph2',
        figure=fig2
    ),
    
    dcc.Graph(
        id='graph3',
        figure=fig3
    )
    # dcc.Graph(
    #     id='graph4',
    #     figure=fig4
    # )

])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

