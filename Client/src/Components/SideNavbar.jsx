import React, { useState, useEffect, useRef } from "react";
import {MDCTextField} from '@material/textfield';
import stocklist from "./stocklist.json"
import { Link } from "react-router-dom";

// const textField = new MDCTextField(document.querySelector('.mdc-text-field'));

export const SideNav = ({ onStockSelect }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [showStockDropdown, setShowStockDropdown] = useState(false);
  const [showCryptoDropdown, setShowCryptoDropdown] = useState(false);
  const [selectedStock, setSelectedStock] = useState("AAPL"); // Default selected stock

  const stockDropdownRef = useRef(null);
  const cryptoDropdownRef = useRef(null);

  function handleToggleSidebar() {
    setCollapsed(!collapsed);
  }

  function toggleStockDropdown() {
    setShowStockDropdown(!showStockDropdown);
  }

  function toggleCryptoDropdown() {
    setShowCryptoDropdown(!showCryptoDropdown);
  }

  function handleStockSelect(symbol) {
    setSelectedStock(symbol); // Update selected stock
    onStockSelect(symbol); // Pass the selected stock up to parent
  }

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        stockDropdownRef.current &&
        !stockDropdownRef.current.contains(event.target) &&
        cryptoDropdownRef.current &&
        !cryptoDropdownRef.current.contains(event.target)
      ) {
        setShowStockDropdown(false);
        setShowCryptoDropdown(false);
      }
    };

    document.addEventListener("click", handleClickOutside);
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  return (
    <div className={`sideNav ${collapsed ? "collapsed" : ""}`}>
      <button onClick={handleToggleSidebar} className="w-full bg-panel rounded-md mb-6 hover:bg-hover text-textSecondary bg-opacity-11">
        Toggle sidebar
      </button>
      
      <div className="flex gap-2 mb-6">
      {['1M', '3M', '6M', '1Y', 'All'].map(range => (
    <button className="bg-panel hover:bg-hover text-xs px-2 py-1 rounded">{range}</button>
        ))}
      </div>

      <button onClick={toggleStockDropdown} className=" w-full bg-panel rounded-md mb-6 hover:bg-hover text-textSecondary bg-opacity-40">
        <Link to="/Stocks" className="text-center">Stocks</Link>
      </button>

      {showStockDropdown && (
        <div ref={stockDropdownRef} className="flex flex-col items-center mb-6">
          <label className="w-full">
            <select onChange={(e) => handleStockSelect(e.target.value)}
               className="w-full text-center border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
            {Object.entries(stocklist).map(([symbol, companyName]) => (
      <option key={symbol} value={symbol}>
        {companyName}
      </option>
    ))}
      
            </select>
          </label>
        </div>   
      )}
      <button onClick  className="w-full bg-panel rounded-md mb-6 hover:bg-hover text-textSecondary bg-opacity-40">
        DOWNLOAD
      </button>
      <select className="mt-2 bg-panel p-1 border border-border text-sm rounded">
      <option>Download as...</option>
      <option value="csv">CSV</option>
      <option value="pdf">PDF</option>
      <option value="json">JSON</option>
      </select>
      <input type="text" placeholder="Search symbol..." className="w-full bg-panel border border-border p-2 text-sm rounded text-textSecondary " />
    </div>
  );
};
