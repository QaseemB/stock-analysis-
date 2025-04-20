from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from datetime import datetime
from stock_analysis.renderers.interactive_plot_renderer import gen_interactive_plt
from stock_analysis.renderers.matplotlib_png_renderer import generate_plots
from stock_analysis.services.csv_file_export import generate_csv_files
from stock_analysis.services.data_retrieval import get_stock_data
from stock_analysis.transfomer.stock_analysis_transformer import analyze_stock_data
from stock_analysis.services.generate_insights import generate_insights




def process_symbol(symbol):
        try:
            print(f'🔎 processing stock symbol: {symbol}')
            cleaned_monthly_data= get_stock_data(symbol)
            if cleaned_monthly_data is None:
                raise ValueError("No data returned")
    
            df = analyze_stock_data(cleaned_monthly_data, symbol)

            if df is None:
                 raise ValueError("Data analysis failed")
    
            plotly_rendering = gen_interactive_plt(symbol,df)
            if plotly_rendering is None:
                raise ValueError("Interactive plot generation failed")
           
            
            png_rendering = generate_plots(symbol,df)
            if png_rendering is None:
                raise ValueError("PNG rendering failed")

            csv_exporting = generate_csv_files(symbol, df)
            if csv_exporting is None:
                raise ValueError("CSV export failed")
    
            insights = generate_insights(df)
            print(f"🧠 Insights for {symbol}:\n{insights}") 

            return{
                "symbol": symbol,
                "plotly_path": plotly_rendering,
                "png_path":png_rendering,
                "csv_path":csv_exporting,
                "insights_path": insights,
                "status": "success"
            }

        except Exception as e:
            return {
                "symbol": symbol,
                "status": "failed",
                "error": str(e)
            }

        
    

def file_generation_parallel(symbols, max_workers=3):
    visual_generator_results = []
    print(f"⚙️ Starting batch with max_workers={max_workers}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_symbol, symbol): symbol for symbol in symbols}

        for future in as_completed(futures):
            result = future.result()
            if not result or 'status' not in result:
                print("⚠️ Unknown result or malformed return value.")
                visual_generator_results.append({
                    "symbol": futures[future],
                    "status": "failed",
                    "error": "Missing status in result"
                })
                continue
            visual_generator_results.append(result)
            print(f"✅ Done: {result['symbol']} — Status: {result['status']} - Error: {result.get('error', 'None')}")

    return visual_generator_results

testing = file_generation_parallel(['QQQ'])

def write_results_to_csv(results, csv_path="generation_summary.csv"):
    keys = ["timestamp", "symbol", "status", "error"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if f.tell() == 0:
            writer.writeheader()  # Only write headers if file is empty

        for res in results:
            writer.writerow({
                "timestamp": timestamp,
                "symbol": res.get("symbol"),
                "status": res.get("status"),
                "error": res.get("error", "")
            })


# write_results_to_csv(testing)