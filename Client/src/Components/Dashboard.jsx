import axios from "axios";
import React, { useState, useEffect } from "react";
import LinePlot from "./LinePlot";

export function Dashboard() {
  return (
    <div className="dashboard-container">
      <div className="lineGraph border-2 border-black">
        <h2>DashBoard</h2>
        <LinePlot data={[1, 2, 3, 4, 5]} />
      </div>

      <div className="test-class">Test</div>
      <div className="bg-blue-500 text-white p-4">
        If you see this, Tailwind is working!
      </div>

      <div className="Profile">
        <h2>Profile</h2>
        <p>StockplaceHolder: random jargin</p>
      </div>
    </div>
  );
}

export default { LinePlot };
