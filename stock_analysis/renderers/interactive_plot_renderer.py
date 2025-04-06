import plotly.express as px
import plotly.io as pio
import pandas as pd
from utils.file_helpers import get_plotly_path

def gen_interactive_plt(symbol, df):
    """
    Generates an interactive Plotly plot and returns its JSON representation.
    """
    # Ensure the index is datetime
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

    color_discrete_map = {
    "close": "blue",
    "moving_avg_3": "red",
    "moving_avg_6": "green",
    "upper_band": "purple",
    "lower_band": "orange"
}

    # Create the Plotly figure
    fig = px.line(
        df,
        x=df.index,
        y=["close", "moving_avg_3", "moving_avg_6", "upper_band", "lower_band"],
        title=f"{symbol} Interactive Stock Analysis",
        color_discrete_map=color_discrete_map
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

    fig_json = pio.to_json(fig)
    plotly_path = get_plotly_path(symbol, "interactive")
    fig.write_html(plotly_path)
    print(f"📊 Plotly HTML saved to: {plotly_path}")


    return fig_json
