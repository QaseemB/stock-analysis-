import plotly.express as px
import plotly.io as pio
import pandas as pd
from stock_analysis.utils.file_helpers import get_plotly_path
from stock_analysis.utils.s3_helper import save_plotly_to_s3, delete_local_file


def gen_interactive_plt(symbol, df, save_html=True, upload_s3=True):
    """
    Generates an interactive Plotly plot and returns its JSON representation.
    """
    # Ensure the index is datetime
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

    color_discrete_map = {
    
    "close": "cyan",
    "moving_avg_3": "coral",
    "moving_avg_6": "green",
    "upper_band": "chocolate",
    "lower_band": "darkblue",
    "rsi": "red",
    # "obv": "gray",
}

    # Create the Plotly figure
    fig = px.line(
        df,
        x=df.index,
        y=["close", "moving_avg_3", "moving_avg_6", "upper_band", "lower_band","rsi"],
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
    s3_uri = None

    if save_html:
        plotly_path = get_plotly_path(symbol, "interactive")
        fig.write_html(plotly_path)
        print(f"📊 Plotly HTML saved to: {plotly_path}")

        if upload_s3:
            s3_uri = save_plotly_to_s3(plotly_path,symbol,"interactive")
            if s3_uri:
                delete_local_file(plotly_path)
                print(f"local path to plotly for {symbol} has been deleted and the file has been uploaded to s3 succefully")




    return {'fig_json':fig_json,
            's3_uri': s3_uri
            }
