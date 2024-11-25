import { useState } from 'react';
import { SideNav } from './Components/SideNavbar';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Dashboard } from './Components/Dashboard';
import './App.css';

function App() {
  const [selectedStock, setSelectedStock] = useState("AAPL"); // Default stock symbol

  const handleStockSelect = (symbol) => {
    setSelectedStock(symbol); // Update the selected stock symbol
  };

  return (
    <>
      <Router>
        <div className="App">
          <SideNav onStockSelect={handleStockSelect} />
          <Routes>
            <Route
              path="/dashboard"
              element={<Dashboard selectedStock={selectedStock} />}
            />
            {/* Other routes can be added here */}
            {/* Use the same Dashboard component for /Stocks */}
            <Route
              path="/Stocks"
              element={<Dashboard selectedStock={selectedStock} />}
            />
          </Routes>
        </div>
      </Router>
    </>
  );
}

export default App;
