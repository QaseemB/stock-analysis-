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
      <button onClick={handleToggleSidebar} className="bg-primary rounded-md mb-6 hover:bg-hover text-textSecondary bg-opacity-40">
        Toggle sidebar
      </button>

      <button onClick={toggleStockDropdown} className="bg-primary rounded-md mb-6 hover:bg-hover text-textSecondary bg-opacity-40">
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
    </div>
  );
};
