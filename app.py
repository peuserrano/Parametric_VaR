import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import datetime as dt

# Import your existing Portfolio class
from src.modelling import Portfolio

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Parametric Portfolio VaR Calculator", className='text-center mb-4'), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(dbc.Label("Tickers (comma separated)"), width=12),
                dbc.Col(dbc.Input(id='tickers', placeholder="Enter ticker symbols (e.g., SPY, BND, GLD)", type='text'), width=12),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Label("Portfolio Value ($)"), width=12),
                dbc.Col(dbc.Input(id='portfolio-value', placeholder="Enter portfolio value", type='number', value=1000000), width=12),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Label("Years of Data"), width=12),
                dbc.Col(dbc.Input(id='years', placeholder="Enter number of years", type='number', value=15), width=12),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Label("Number of Days for VaR"), width=12),
                dbc.Col(dbc.Input(id='days', placeholder="Enter number of days for VaR calculation", type='number', value=5), width=12),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Label("Confidence Levels (%)"), width=12),
                dbc.Col(dbc.Checklist(
                    options=[
                        {'label': '90%', 'value': 0.9},
                        {'label': '95%', 'value': 0.95},
                        {'label': '99%', 'value': 0.99},
                    ],
                    value=[0.9, 0.95, 0.99],
                    id='confidence-levels',
                    inline=True,
                ), width=12),
            ], className="mb-3"),
            dbc.Button("Calculate VaR", id='calculate-btn', color='primary', className='mt-3')
        ], width=4),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Value at Risk (VaR)", className='card-title'),
                    html.Div(id='var-output')
                ])
            ]),
            dcc.Graph(id='var-histogram')
        ], width=8)
    ])
], fluid=True)


# Callback for handling the VaR calculation and plot
@app.callback(
    [Output('var-output', 'children'),
     Output('var-histogram', 'figure')],
    [Input('calculate-btn', 'n_clicks')],
    [State('tickers', 'value'),
     State('portfolio-value', 'value'),
     State('years', 'value'),
     State('days', 'value'),
     State('confidence-levels', 'value')]
)
def update_var(n_clicks, tickers, portfolio_value, years, days, confidence_levels):
    if n_clicks is None:
        return "", {}

    # Handle ticker input and create the portfolio object
    ticker_list = [t.strip() for t in tickers.split(',')]
    
    # Create an instance of the Portfolio class
    portfolio = Portfolio(tickers=ticker_list, portfolio_value=portfolio_value, years=years)
    
    # Calculate the VaR
    VaRs = portfolio.calculate_parametric_var(days=days, confidence_levels=confidence_levels)
    
    # Prepare VaR output
    var_output = html.Ul([
        html.Li(f"{int(cl * 100)}% Confidence Level: ${VaRs[cl]:,.2f}")
        for cl in confidence_levels
    ])

    # Plot the histogram
    fig = go.Figure()
    
    # Historical returns
    historical_returns = portfolio.calculate_historical_returns(days=days)
    historical_x_day_returns_dollar = historical_returns * portfolio_value
    
    # Add histogram
    fig.add_trace(go.Histogram(x=historical_x_day_returns_dollar, nbinsx=50, name=f'{days}-Day Returns', opacity=0.6))
    
    # Add VaR lines
    for cl in confidence_levels:
        fig.add_vline(x=-VaRs[cl], line=dict(color='red', dash='dash'), annotation_text=f'{int(cl*100)}% VaR', annotation_position='top right')

    # Configure layout
    fig.update_layout(
        title=f'Distribution of Portfolio {days}-Day Returns and VaR',
        xaxis_title=f'{days}-Day Portfolio Return ($)',
        yaxis_title='Frequency',
        showlegend=False
    )

    return var_output, fig


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
