import plotly.express as px
import plotly.io as pio
import pandas as pd

def gen_interactive_plt(symbol, df):
    """
    Generates an interactive Plotly plot and returns its JSON representation.
    """
    # Ensure the index is datetime
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

    # Create the Plotly figure
    fig = px.line(
        df,
        x=df.index,
        y=["close", "moving_avg_3", "moving_avg_6", "upper_band", "lower_band"],
        title=f"{symbol} Interactive Stock Analysis"
    )

    # Update layout with proper titles and formatting
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis=dict(
            tickformat="%Y-%m-%d",
            tickangle=45
        )
    )

    # Convert the Plotly figure to JSON
    return pio.to_json(fig)  # This JSON can be passed to React for rendering
