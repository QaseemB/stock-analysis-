from stock_analysis.renderers.interactive_plot_renderer import gen_interactive_plt
from stock_analysis.renderers.matplotlib_png_renderer import generate_plots
from stock_analysis.services.csv_file_export import generate_csv_files
from stock_analysis.services.data_retrieval import get_stock_data
from stock_analysis.transfomer.stock_analysis_transformer import analyze_stock_data
from stock_analysis.services.generate_insights import generate_insights



def file_generation(symbol):
    cleaned_monthly_data= get_stock_data(symbol)
    if cleaned_monthly_data is None:
        print(f"Error: no data returned for symbol {symbol}")
        return None
    df = analyze_stock_data(cleaned_monthly_data, symbol)

    if df is None:
        print(f"Error: Analysis failed in analyze_stock_data for {symbol}")
        return None
    
    plotly_rendering = gen_interactive_plt(symbol,df)
    if plotly_rendering is None:
        print(f"Error: plotly rendering has failed for {symbol}")
        return None

    png_rendering = generate_plots(symbol,df)
    if png_rendering is None:
        print(f"Error: png rendering has faile for {symbol}")
        return None

    csv_exporting = generate_csv_files(symbol, df)
    if csv_exporting is None:
        print (f"Error: csv exportation had failed for {symbol}")
        return None
    
    insights = generate_insights(df)
    print(f"🧠 Insights for {symbol}:\n{insights}") 
    
    print(f"All files for symbol: {symbol} has generated sucessfully")
    
    return plotly_rendering, png_rendering, csv_exporting, insights

# testing = file_generation('TSLA')

