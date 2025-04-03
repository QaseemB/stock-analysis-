import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";

export const SideNav = ({ onStockSelect }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [showStockDropdown, setShowStockDropdown] = useState(false);
  const [showCryptoDropdown, setShowCryptoDropdown] = useState(false);
  const [selectedStock, setSelectedStock] = useState("AAPL"); // Default selected stock

  const stockDropdownRef = useRef(null);
  const cryptoDropdownRef = useRef(null);


  const stockOptions = {
  AAPL: "Apple",
  GOOG: "Google",
  MSFT: "Microsoft",
  AMZN: "Amazon",
  META: "Meta", 
  IBM: "IBM",
  TSLA: "Tesla",
  NVDA: "NVIDIA",
  AVGO: "Broadcom Inc.",
  TSM: "Taiwan Semiconductor",
  JPM: "JP Morgan",
  MA: "Mastercard",
  COST: "Costco",
  PG: "Procter & Gamble",
  NFLX: "Netflix",
  JNJ: "Johnson & Johnson",
  BAC: "Bank of America",
  CRM: "Salesforce Inc.",
  TM: "Toyota",
  KO: "Coca-Cola",
  ORCL: "Oracle",
  D: "Dominion Energy",
  HD: "Home Depot",
  ABBV: "AbbVie",
  PLTR: "Palantir Technologies",
  ABT: "Abbott Laboratories",
  MRK: "Merck & Co.",
  AXP: "American Express",
  QCOM: "Qualcomm",
  ADBE: "Adobe",
  AMD: "Advanced Micro Devices",
  T: "AT&T",
  VZ: "Verizon",
  DIS: "Disney",
  NKE: "Nike",
  PFE: "Pfizer",
  PEP: "PepsiCo",
  CSCO: "Cisco",
  CMCSA: "Comcast",
  XOM: "ExxonMobil",
  WMT: "Walmart",
  BMY: "Bristol-Myers Squibb",
  INTC: "Intel",
  UNH: "UnitedHealth Group",
  CVX: "Chevron",
  LLY: "Eli Lilly",
  MCD: "McDonald's",
  HON: "Honeywell",
  NEE: "NextEra Energy",
  TXN: "Texas Instruments",
  PM: "Philip Morris",
  LOW: "Lowe's",
  UPS: "United Parcel Service",
  SCHW: "Charles Schwab",
  MS: "Morgan Stanley",
  AMGN: "Amgen",
  CAT: "Caterpillar",
  GS: "Goldman Sachs",
  RTX: "Raytheon Technologies",
  SPGI: "S&P Global",
  BLK: "BlackRock",
  BKNG: "Booking Holdings",
  ISRG: "Intuitive Surgical",
  MDT: "Medtronic",
  SYK: "Stryker",
  LMT: "Lockheed Martin",
  DE: "Deere & Co.",
  ADP: "Automatic Data Processing",
  NOW: "ServiceNow",
  TMO: "Thermo Fisher Scientific",
  UNP: "Union Pacific",
  AMT: "American Tower",
  CB: "Chubb",
  CCI: "Crown Castle",
  ZTS: "Zoetis",
  GILD: "Gilead Sciences",
  FIS: "Fidelity National Information Services",
  EL: "Estee Lauder",
  MO: "Altria Group",
  DUK: "Duke Energy",
  SO: "Southern Company",
  MMM: "3M",
  BDX: "Becton Dickinson",
  APD: "Air Products & Chemicals",
  C: "Citigroup",
  USB: "U.S. Bancorp",
  PNC: "PNC Financial Services",
  CL: "Colgate-Palmolive",
  DHR: "Danaher",
  ITW: "Illinois Tool Works",
  WM: "Waste Management",
  SHW: "Sherwin-Williams",
  ECL: "Ecolab",
  FISV: "Fiserv",
  AON: "Aon",
  HUM: "Humana",
  PSA: "Public Storage",
  NSC: "Norfolk Southern",
  ETN: "Eaton",
  ROP: "Roper Technologies",
  MAR: "Marriott International",
  KMB: "Kimberly-Clark",
  AEP: "American Electric Power",
  SBUX: "Starbucks",
  LRCX: "Lam Research",
  ATVI: "Activision Blizzard",
  ORLY: "O'Reilly Automotive",
  MCO: "Moody's",
  KLAC: "KLA Corporation",
  CTAS: "Cintas",
  EQIX: "Equinix",
  ILMN: "Illumina",
  REGN: "Regeneron Pharmaceuticals",
  IDXX: "IDEXX Laboratories",
  MTD: "Mettler-Toledo",
  CDNS: "Cadence Design Systems",
  SNPS: "Synopsys",
  FTNT: "Fortinet",
  PAYC: "Paycom Software",
  ANSS: "ANSYS",
  VRSK: "Verisk Analytics",
  MSCI: "MSCI Inc.",
  FLT: "FleetCor Technologies",
  CPRT: "Copart",
  TDG: "TransDigm Group",
  WST: "West Pharmaceutical Services",
  RMD: "ResMed",
  ALGN: "Align Technology",
  STE: "STERIS",
  TECH: "Bio-Techne",
  BIO: "Bio-Rad",
  TER: "Teradyne",
  KEYS: "Keysight Technologies",
  HUBS: "HubSpot",
  SEDG: "SolarEdge Technologies",
  ENPH: "Enphase Energy",
  TEAM: "Atlassian",
  OKTA: "Okta",
  ZS: "Zscaler",
  CRWD: "CrowdStrike",
  DDOG: "Datadog",
  DOCU: "DocuSign",
  FSLY: "Fastly",
  NET: "Cloudflare",
  PLUG: "Plug Power",
  BLD: "TopBuild",
  PTON: "Peloton",
  ROKU: "Roku",
  SQ: "Block (formerly Square)",
  TWLO: "Twilio",
  U: "Unity Software",
  ZM: "Zoom Video",
  ZSAN: "Zosano Pharma"
};

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
        <div ref={stockDropdownRef} className="flex flex-col items-center mb-6">
          <label className="w-full">
            <select onChange={(e) => handleStockSelect(e.target.value)}
               className="w-full text-center border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
            {Object.entries(stockOptions).map(([symbol, companyName]) => (
      <option key={symbol} value={symbol}>
        {companyName}
      </option>
    ))}
      
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
