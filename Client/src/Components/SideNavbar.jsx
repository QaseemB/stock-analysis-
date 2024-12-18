import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";

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
      <button onClick={handleToggleSidebar} className="bg-cyan-500 mb-6 hover:bg-sky-700">
        Toggle sidebar
      </button>

      <button onClick={toggleStockDropdown} className="bg-red-500 mb-4 hover:bg-red-700">
        <Link to="/Stocks" className="text-center">Stocks</Link>
      </button>

      {showStockDropdown && (
        <div ref={stockDropdownRef} className="flex flex-col mb-6">
          <label>
            <select onChange={(e) => handleStockSelect(e.target.value)}>
              <option value="AAPL">Apple</option>
              <option value="TSLA">Tesla</option>
              <option value="GOOG">Google</option>
              <option value="AMZN">Amazon</option>
              <option value="MSFT">Microsoft</option>
              <option value="META">Meta</option>
              <option value="IBM">IBM</option>
              <option value="NVDA">NVIDIA</option>
              <option value="AVGO">AVGO</option>
              <option value="TSM">TSM</option>
              <option value="JPM">JPM</option>
              <option value="MA">MA</option>
              <option value="COST">COST</option>
              <option value="PG">PG</option>
              <option value="NFLX">NFLX</option>
              <option value="JNJ">JNJ</option>
              <option value="BAC">BAC</option>
              <option value="CRM">CRM</option>
              <option value="TM">TM</option>
              <option value="KO">KO</option>
            </select>
          </label>
        </div>
      )}

      <button onClick={toggleCryptoDropdown} className="bg-red-500 mb-2">
        <Link to="/Crypto" className="text-center">Crypto</Link>
      </button>
      {showCryptoDropdown && (
        <div ref={cryptoDropdownRef} className="flex flex-col mb-6">
          <label>
            <select>
              <option value="BTC">Bitcoin</option>
              <option value="ETH">Ethereum</option>
              <option value="DOGE">DOGE</option>
              <option value="SHIB">Shiba-Inu</option>
              <option value="SOL">Solana</option>
              <option value="USDT">Tether</option>
              <option value="XRP">Ripple</option>
            </select>
          </label>
        </div>
      )}
    </div>
  );
};
