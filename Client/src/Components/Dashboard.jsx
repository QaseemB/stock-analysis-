import axios from "axios";
import React, { useState, useEffect } from "react";
import LinePlot from "./LinePlot";

const stockSymbols = ["AAPL", "GOOG", "MSFT", "AMZN", "META", "IBM", "TSLA"];

export function Dashboard() {
  const [dummydata, setDummydata] = useState([]); // State to store the monthly data
  const [loading, setLoading] = useState(true);  // State to track the loading status
  const [error, setError] = useState(null);  // State to track the error status

  useEffect(() => {
    const fetchStockData = async (symbol) => {
      try {
        const response = await axios.get(
          `http://localhost:3030/api/stock/MSFT`);
          const monthlyData = response.data?.monthlyData;
         if (monthlyData) {
        setDummydata(monthlyData); // Assuming the API response has the stock data
         } else {
            throw new Error("unexpected response structure");
         }
      } catch (err) {
        setError(err.message || "Error fetching data");
      }finally{
        setLoading(false); // Always stop loading, regardless of success or failure
      }
        
      };
    fetchStockData();
  }, []); // Empty dependency array ensures it runs once when the component mounts

    // Render Logic
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  const  fetchStockDataWithRateLimiting = async (symbols) => {
  for (const symbol of  symbols) {
    await fetchstock(symbol);
    // delay for 15 seconds to comply with 5 requests per minute
    // await delay(15000);
  }
};
  return (
    <div className="dashboard-container ml-[20%]">
      {/* Dashboard Title */}
      <div className="dashboard-title text-center block">
        <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      </div>
      {/* Dashboard Content */}
      <div className="dashboard-content flex justify-between gap-8">
        <div className="lineGraph border-4 rounded-lg w-3/6">
          <h2 className="text-center">Analysis</h2>
          <LinePlot data={dummydata} />
        </div>
        {/* Profile */}
        <div className="Profile border-2">
          <h2>Profile</h2>
          <p>StockplaceHolder: random jargin</p>
        </div>
      </div>
    </div>
  );
}

export default { LinePlot };
