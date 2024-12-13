import axios from "axios";
import React, { useState, useEffect } from "react";
import LinePlot from "./LinePlot";

export function Dashboard({ selectedStock }) {
  const [dummydata, setDummydata] = useState([]); // Store stock data
  const [summaryData, setSummaryData] = useState({})
  const [loading, setLoading] = useState(true);  // Loading status
  const [error, setError] = useState(null);  // Error status

  useEffect(() => {
    const fetchStockData = async (symbol) => {
      try {
        const response = await axios.get(`http://localhost:3030/api/stock/${symbol}`);
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
      }
    };

    if (selectedStock) {
      fetchStockData(selectedStock);
    }
  }, [selectedStock]); // Re-fetch data whenever the stock symbol changes

  useEffect(()=>{
    const fetchFlaskData = async (symbol) =>{
      try{
        const response = await axios.get(`http://localhost:3030/api/stock-analysis/${symbol}`)
        const summary= response.data?.summary;
        if (summary){
          setSummaryData(summary);
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

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  
  const latestDate = new Date(summaryData.latest_date);
  const formattedDate = latestDate.toLocaleDateString("en-GB", {
  year: 'numeric',
  month: 'short',
  day: 'numeric',
  timeZone: 'UTC',
});
console.log(formattedDate); 

  return (
    <div className="dashboard-container ml-[15%]">
      <div className="dashboard-title text-center block">
        <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      </div>
      <div className="dashboard-content flex justify-between ">
        <div className="lineGraph border-4 rounded-lg w-3/6">
          <h2 className="text-center">{selectedStock} Analysis</h2>
          <LinePlot data={dummydata} />
        </div>
        <div className="Profile border-2">
          <h2 className="text-center">STOCK SUMMARY FOR {selectedStock}</h2>
          <p className="tracking-wide leading-8">As of {formattedDate}, the latest data shows that {selectedStock} opened at ${summaryData.latest_open} and closed at ${summaryData.latest_close}. The monthly return for the stock stands at {summaryData.monthly_return}%, reflecting its recent performance. The 6-month moving average is {summaryData.moving_avg_6}, providing a broader view of the stock's trend, while the 3-month moving average is {summaryData.moving_avg_3}, offering a more short-term perspective on its movement.

This analysis provides valuable insights into the stock's current performance and trend over multiple timeframes.</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
