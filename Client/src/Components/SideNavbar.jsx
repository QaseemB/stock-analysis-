import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";

export const SideNav = (props) => {
  const [collapsed, setCollapsed] = useState(false);
  const [showStockDropdown, setShowStockDropdown] = useState(false); // State for managing the dropdown visibility
  const [showCryptoDropdown, setShowCryptoDropdown] = useState(false); // State for

  const stockDropdownRef = useRef(null); // Reference for the stock dropdown
  const cryptoDropdownRef = useRef(null); // Reference for the crypto dropdown


  function handleToggleSidebar() {
    setCollapsed(!collapsed);
  }

  function toggleStockDropdown() {
    setShowStockDropdown(!showStockDropdown); // Toggle dropdown visibility when "Stocks" is clicked
  }
  function toggleCryptoDropdown() {
    setShowCryptoDropdown(!showCryptoDropdown); // Toggle dropdown visibility when "Cryptok"
  }

  // Close dropdown if click happens outside the dropdown
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

    // Clean up the event listener when component unmounts
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  return (
    <div className={`sideNav ${collapsed ? "collapsed" : ""}  `}>
      <button
        onClick={handleToggleSidebar}
        className="bg-cyan-500 mb-6 hover:bg-sky-700 "
      >
        Toggle sidebar
      </button>

      {/* Stocks link with a dropdown */}
      <button
        onClick={toggleStockDropdown}
        className="bg-red-500 mb-4 hover:bg-red-700"
      >
        <Link to="/Stocks" className="text-center">
          Stocks
        </Link>
      </button>

      {/* Conditionally render the dropdown based on the state */}
      {showStockDropdown && (
        <div ref={stockDropdownRef} className="flex flex-col mb-6">
          <label>
            <select>
              <option value="AAPL">Apple</option>
              <option value="TSLA">Tesla</option>
              <option value="GOOG">Google</option>
              <option value="AMZN">Amazon</option>
              <option value="MSFT">Microsoft</option>
              <option value="META">Meta</option>
              <option value="IBM">IBM</option>
            </select>
          </label>
        </div>
      )}

      {/* Crypto link with a dropdown */}
      <button onClick={toggleCryptoDropdown} className="bg-red-500 mb-2">
        <Link to="/Crypto" className="text-center">
          Crypto
        </Link>
      </button>
      {/* Conditionally render the dropdown based on the state */}
      {showCryptoDropdown && (
        <div ref={cryptoDropdownRef} className="flex flex-col mb-6">
          <label>
            <select>
              <option value="BTC">Bitcoin</option>
              <option value="ETH">Etherum</option>
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
