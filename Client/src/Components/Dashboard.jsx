import axios from "axios";
import React, { useState, useEffect } from "react";
import LinePlot from "./LinePlot";

export function Dashboard({ selectedStock }) {
  const [dummydata, setDummydata] = useState([]); // Store stock data
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

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="dashboard-container ml-[15%]">
      <div className="dashboard-title text-center block">
        <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      </div>
      <div className="dashboard-content flex justify-between gap-8">
        <div className="lineGraph border-4 rounded-lg w-3/6">
          <h2 className="text-center">{selectedStock} Analysis</h2>
          <LinePlot data={dummydata} />
        </div>
        <div className="Profile border-2">
          <h2>Profile</h2>
          <p>StockplaceHolder: random jargon</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
