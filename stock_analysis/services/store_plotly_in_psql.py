from stock_analysis.renderers.interactive_plot_renderer import gen_interactive_plt
from stock_analysis.utils.upsert_plotly import upsert_plotly
from stock_analysis.services.data_retrieval import get_stock_data
from stock_analysis.transfomer.stock_analysis_transformer import analyze_stock_data

def plotly_insert_into_psql(symbols: list):
    """
    Generates and stores Plotly charts for a list of stock symbols.
    Returns a list of result dictionaries (per symbol).
    """
    plotly_results = []
    for symbol in symbols:
        try:
            cleaned_monthly_data= get_stock_data(symbol)
            if cleaned_monthly_data is None:
                raise ValueError("No data returned")
    
            df = analyze_stock_data(cleaned_monthly_data, symbol)

            if df is None:
                raise ValueError("Data analysis failed")
    
            plotly_rendering = gen_interactive_plt(symbol,df, save_html=False, upload_s3=False)

            if plotly_rendering is None:
                raise ValueError("Interactive plot generation failed")
            
            fig_json = plotly_rendering['fig_json']
            insertion = upsert_plotly(symbol, fig_json)

            plotly_results.append({
                "symbol": symbol,
                "status": "success",
                "insertion": insertion
            })
   
            print(f"✅ Inserted Plotly chart for {symbol}")

        except Exception as e:
            plotly_results.append({
                "symbol": symbol,
                "status": "failed",
                "error": str(e)
            })

            print(f"❌ Failed for {symbol}: {e}")
    return plotly_results
    
plotly_insert_into_psql(['TSM','BAC','VOO', 'AMZN', 'META'])