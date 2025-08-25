
import os
import io
import base64
import pandas as pd
import psycopg2
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# --- CONFIGURATION ---
DB_HOST = "localhost"
DB_NAME = "real_estate_db"
DB_USER = "etl_user"
DB_PASSWORD = "etl_password" # Change this to your password.
# The table name is now different to reflect that it contains all cleaned data.
DB_TABLE = "real_estate_data"

# --- DATABASE CONNECTION ---
def fetch_data_from_db():
    """Fetches all data from the PostgreSQL table and returns it as a Pandas DataFrame."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        # Fetch all columns from the new table
        query = f"SELECT * FROM {DB_TABLE}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"❌ Error fetching data from database: {e}")
        # Return an empty DataFrame on error to prevent the app from crashing
        return pd.DataFrame(columns=['house_age', 'distance_to_mrt', 'convenience_stores', 'latitude', 'longitude', 'house_price'])

# Fetch data once when the app starts
df_initial = fetch_data_from_db()

# --- FUNCTION TO CREATE INITIAL GRAPHS ---
def create_initial_graphs():
    """Creates the initial, unfiltered graphs for the app layout."""
    
    # Create the initial Bar Chart
    fig_bar = px.bar(
        df_initial.groupby('convenience_stores')['house_price'].mean().reset_index(),
        x='convenience_stores',
        y='house_price',
        title="Average House Price per Unit Area",
        labels={'convenience_stores': 'Number of Convenience Stores', 'house_price': 'Average Price'},
        color_continuous_scale='Viridis'
    )
    fig_bar.update_traces(marker_color='#5B8FB9')
    fig_bar.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        title_font_size=16, margin=dict(t=40, b=40, l=40, r=40),
        font=dict(family="Montserrat, sans-serif")
    )

    # Create the initial Scatter Plot
    fig_scatter = px.scatter(
        df_initial,
        x='distance_to_mrt',
        y='house_price',
        title="House Price vs. Distance to MRT Station",
        labels={'distance_to_mrt': 'Distance to MRT (meters)', 'house_price': 'House Price per Unit Area'},
        color='house_age',
        size='convenience_stores',
        hover_data=['convenience_stores', 'house_age'],
        color_continuous_scale='Plasma'
    )
    fig_scatter.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        title_font_size=16, margin=dict(t=40, b=40, l=40, r=40),
        font=dict(family="Montserrat, sans-serif")
    )

    return fig_bar, fig_scatter

# Create initial figures
initial_bar_fig, initial_scatter_fig = create_initial_graphs()

# --- DASHBOARD LAYOUT ---
app = Dash(__name__)

app.layout = html.Div(
    className="bg-gray-100 p-8 min-h-screen font-sans",
    children=[
        # Title and description
        html.Div(className="max-w-6xl mx-auto text-center mb-10 p-6 rounded-xl shadow-md bg-white", children=[
            html.H1("Find your dream home, powered by data", className="text-4xl font-bold text-gray-800 mb-2"),
            html.P("Want to know what really drives a property's value? Our dashboard lets you explore the data yourself, revealing the hidden connections between price and features like nearby convenience stores or the age of a house. It's not just a chart; it's a conversation with the market.", className="text-lg text-gray-600"),
        ]),

        # Interactive components (Filters)
        html.Div(
            className="bg-white p-6 rounded-lg shadow-lg mb-8 max-w-6xl mx-auto",
            children=[
                html.H3("Interactive Filters", className="text-2xl font-semibold mb-4 text-gray-700"),
                html.Div(className="grid grid-cols-1 md:grid-cols-2 gap-6", children=[
                    # Slider for Convenience Stores
                    html.Div(children=[
                        html.P("Filter by Number of Convenience Stores", className="font-medium text-gray-500 mb-2"),
                        dcc.RangeSlider(
                            id='store-slider',
                            min=df_initial['convenience_stores'].min(),
                            max=df_initial['convenience_stores'].max(),
                            step=1,
                            value=[df_initial['convenience_stores'].min(), df_initial['convenience_stores'].max()],
                            marks={int(i): {'label': str(int(i)), 'style': {'font-family': 'Montserrat'}} for i in df_initial['convenience_stores'].unique()},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ]),
                    # Slider for House Age
                    html.Div(children=[
                        html.P("Filter by House Age", className="font-medium text-gray-500 mb-2"),
                        dcc.RangeSlider(
                            id='age-slider',
                            min=df_initial['house_age'].min(),
                            max=df_initial['house_age'].max(),
                            step=1,
                            value=[df_initial['house_age'].min(), df_initial['house_age'].max()],
                            marks={int(i): {'label': str(int(i)), 'style': {'font-family': 'Montserrat'}} for i in df_initial['house_age'].unique()},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                    ]),
                ]),
            ]
        ),

        # The main plots
        html.Div(
            className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-6xl mx-auto",
            children=[
                # Plot 1: Scatter plot for price vs distance to MRT
                html.Div(className="bg-white p-6 rounded-lg shadow-lg", children=[
                    dcc.Graph(id='price-scatter-chart', style={'height': '450px'}, figure=initial_scatter_fig)
                ]),
                # Plot 2: Bar chart for price vs convenience stores
                html.Div(className="bg-white p-6 rounded-lg shadow-lg", children=[
                    dcc.Graph(id='price-bar-chart', style={'height': '450px'}, figure=initial_bar_fig)
                ])
            ]
        )
    ]
)

# --- CALLBACKS (INTERACTIVITY LOGIC) ---
@app.callback(
    Output('price-bar-chart', 'figure'),
    Output('price-scatter-chart', 'figure'),
    Input('store-slider', 'value'),
    Input('age-slider', 'value')
)
def update_graphs(selected_stores, selected_age):
    """Updates both charts based on the selected range of convenience stores and house age."""
    # Filter the DataFrame based on the slider's values
    filtered_df = df_initial[
        (df_initial['convenience_stores'] >= selected_stores[0]) &
        (df_initial['convenience_stores'] <= selected_stores[1]) &
        (df_initial['house_age'] >= selected_age[0]) &
        (df_initial['house_age'] <= selected_age[1])
    ]

    # Create the first plot: Bar Chart (Average Price vs. Convenience Stores)
    # We use a try-except block to handle cases where the filter returns an empty DataFrame
    if filtered_df.empty:
        fig_bar = px.bar(title="No data to display.")
    else:
        fig_bar = px.bar(
            filtered_df.groupby('convenience_stores')['house_price'].mean().reset_index(),
            x='convenience_stores',
            y='house_price',
            title="Average House Price per Unit Area",
            labels={'convenience_stores': 'Number of Convenience Stores', 'house_price': 'Average Price'},
            color_continuous_scale='Viridis'
        )
        fig_bar.update_traces(marker_color='#5B8FB9')
        fig_bar.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            title_font_size=16, margin=dict(t=40, b=40, l=40, r=40),
            font=dict(family="Montserrat, sans-serif"),
        )

    # Create the second plot: Scatter Plot (Price vs. Distance to MRT)
    if filtered_df.empty:
        fig_scatter = px.scatter(title="No data to display.")
    else:
        fig_scatter = px.scatter(
            filtered_df,
            x='distance_to_mrt',
            y='house_price',
            title="House Price vs. Distance to MRT Station",
            labels={'distance_to_mrt': 'Distance to MRT (meters)', 'house_price': 'House Price per Unit Area'},
            color='house_age',
            size='convenience_stores',
            hover_data=['convenience_stores', 'house_age'],
            color_continuous_scale='Plasma'
        )
        fig_scatter.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            title_font_size=16, margin=dict(t=40, b=40, l=40, r=40),
            font=dict(family="Montserrat, sans-serif"),
        )

    return fig_bar, fig_scatter

# --- RUN SERVER ---
if __name__ == '__main__':
    # You must have your PostgreSQL database running and your table populated
    # by running the extract, transform, and load scripts first.
    app.run(debug=True)
