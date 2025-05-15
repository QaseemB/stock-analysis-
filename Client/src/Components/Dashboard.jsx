import axios from "axios";
import React, { useState, useEffect } from "react";
import Plot from "react-plotly.js";
import LinePlot from "./LinePlot";
export function Dashboard({ selectedStock }) {
  const [dummydata, setDummydata] = useState([]); // Store stock data
  const [summaryData, setSummaryData] = useState({});
  const [plotData, setPlotData] = useState({});
  const [loading, setLoading] = useState(true); // Loading status
  const [error, setError] = useState(null); // Error status
  const [flaskLoading, setFlaskLoading] = useState(true);
  const [stockError, setStockError] = useState(null);
  const [flaskError, setFlaskError] = useState(null);

  const s3Bucket = import.meta.env.VITE_APP_S3_BUCKET || "default-bucket-name";

  useEffect(() => {
    const fetchStockData = async (symbol) => {
      try {
        const response = await axios.get(`http://localhost:3030/api/stock/${selectedStock}`);
        const monthlyData = response.data?.monthlyData;
        if (monthlyData) {
          setDummydata(monthlyData); // Set stock data
        } else {
          throw new Error("Unexpected response structure");
        }
      } catch (err) {
        setError(err.message || "Error fetching data");
      } finally {
        setLoading(false);
        setFlaskLoading(false);
      }
    };

    if (selectedStock) {
      fetchStockData(selectedStock);
    }
  }, [selectedStock]); // Re-fetch data whenever the stock symbol changes

  useEffect(()=>{
    const fetchFlaskData = async (symbol) =>{
      try{
        setFlaskLoading(true)
        const response = await axios.get(`https://${s3Bucket}.s3.amazonaws.com/STOCKMARKET_FBS/${selectedStock}/summary/${selectedStock}_report.json`)

        const summary = response.data
        if (summary) {
          setSummaryData(summary);
          // setPlotData(plot);
          console.log('summary response:',summary)
        } else {
          throw new Error("Unexpected response structure");
        }
      } catch (err) {
        setError(err.message || "Error fetching data");
      } finally {
        setLoading(false);
      }
    };
    if (selectedStock) {
      fetchFlaskData(selectedStock);
    }
  }, [selectedStock]);

  useEffect(() => {
    const fetchPlotlyDataFromS3 = async () => {
      try {
        setFlaskLoading(true);
        // console.log(`Fetching from: https://${s3Bucket}.s3.amazonaws.com/interactive_plots/${selectedStock}.json`);

        const response = await axios.get(
          `https://${s3Bucket}.s3.amazonaws.com/STOCKMARKET_FBS/${selectedStock}/plotly/${selectedStock}_plotly_psql_.json`
        );
        console.log("Raw S3 Response:", response);

        if (!response.data || !response.data.data || !response.data.layout) {
          throw new Error("Invalid Plotly JSON structure");
        }

      setPlotData(response.data); // Store the fetched data
      setFlaskLoading(false);
    } catch (err) {
      console.error("Error fetching Plotly data from S3:", err);
      setFlaskError(err.message || "Error fetching plot data from S3");
      setFlaskLoading(false);
    }
  };

    if (selectedStock) {
      fetchPlotlyDataFromS3();
    }
  }, [selectedStock, s3Bucket]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  const latestDate = new Date(summaryData.latest_date);
  const formattedDate = latestDate.toLocaleDateString("en-GB", {
    year: "numeric",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  });

  const bollingerPath = `https://${s3Bucket}.s3.amazonaws.com/STOCKMARKET_FBS/${selectedStock}/png/${selectedStock}_bollinger_plot.png`;
  const movingAveragePath = `https://${s3Bucket}.s3.amazonaws.com/STOCKMARKET_FBS/${selectedStock}/png/${selectedStock}_moving_avg_plot.png`;
  const tradingVolumePath = `https://${s3Bucket}.s3.amazonaws.com/STOCKMARKET_FBS/${selectedStock}/png/${selectedStock}_volume_plot.png`;
  const macdPath = `https://${s3Bucket}.s3.amazonaws.com/STOCKMARKET_FBS/${selectedStock}/png/${selectedStock}_macd_plot.png`;
  const plotUrl = `https://${s3Bucket}.s3.amazonaws.com/STOCKMARKET_FBS/${selectedStock}/plotly/${selectedStock}_plotly_psql.json`;
  // console.log("S3 Bucket URL:", plotUrl);

  return (
    <div className="dashboard-container ml-[15%]">
      <div className="dashboard-title text-center block">
        <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      </div>
      <div className="debug p-2 bg-gray-100 text-xs">
  <p>flaskLoading: {flaskLoading.toString()}</p>
  <p>plotData ready: {plotData?.data?.length > 0 ? "✅" : "❌"}</p>
  <p>layout ready: {plotData?.layout ? "✅" : "❌"}</p>
</div>
      <div className="dashboard-content grid grid-cols-2 gap-4 ">
           <div className="linegraph plot border-2 flex">
  {flaskLoading ? (
    <div>Loading...</div>
  ) : plotData?.data && plotData?.layout ? (
    <Plot
      data={plotData.data} // Use data from S3
      layout={{
        ...plotData.layout,
        autosize: true,
        width: undefined,
        height: 400,
        responsive: true,
        margin: { l: 50, r: 50, t: 50, b: 50 },
      }}
      config={{ responsive: true }}
      style={{ width: "100%", maxWidth: "600px", margin: "auto" }}
    />
  ) : (
    <div>Error loading chart data</div>
  )}
</div>
       
        <div className="Profile border-2 p-4">
          <h2 className="text-center">STOCK SUMMARY FOR {selectedStock}</h2>
          <p className="tracking-wide leading-8">
            As of {formattedDate}, the latest data shows that {selectedStock}{" "}
            opened at ${summaryData.latest_open} and closed at $
            {summaryData.latest_close}. The monthly return for the stock stands
            at {summaryData.monthly_return}%, reflecting its recent performance.
            The 6-month moving average is {summaryData.moving_avg_6}, providing
            a broader view of the stock's trend, while the 3-month moving
            average is {summaryData.moving_avg_3}, offering a more short-term
            perspective on its movement. This analysis provides valuable
            insights into the stock's current performance and trend over
            multiple timeframes.
          </p>
        </div>

        <div className="bollinger-graph border-2 p-4">
          <h2 className="text-center">Bollinger bands for {selectedStock}</h2>
          <img
            src={`${bollingerPath}`}
            style={{ width: "100%", maxWidth: "600px", margin: "auto" }}
          />
        </div>
        <div className="trading-volume border-2 p-4">
          <h2 className="text-center">Trading Volume for {selectedStock}</h2>
          <img
            src={`${tradingVolumePath}`}
            style={{ width: "100%", maxWidth: "600px", margin: "auto" }}
          />
        </div>
        <div className="macd border-2 p-4">
          <h2 className="text-center">MACD for {selectedStock}</h2>
          <img
            src={`${macdPath}`}
            style={{ width: "100%", maxWidth: "600px", margin: "auto" }}
          />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
