import React, { useState } from 'react'
import { Link } from 'react-router-dom'


export const SideNav = (props) => {
    const [collapsed, setCollapsed] = useState(false);
    function handleToggleSidebar() {
    setCollapsed(!collapsed);
}
return (
    <div className={`sideNav ${collapsed ? 'collapsed' : ''}`}>
        <button onClick={handleToggleSidebar}>Toggle sidebar</button>
        <Link to="/Stocks">Stocks
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
        </Link>
        <Link to="Crypto">Crypto</Link>
            <label>
                <select>
                    <option value="BTC">Bitcoin</option>
                    <option value="DOGE"> Dogecoin</option>
                    <option value="ETH">Ethereum</option>
                    <option value="SOL">Solana</option>
                    <option value="XRP">Ripple</option>
                    <option value="SHIB">Shiba-Inu</option>
                    <option value="USDT">Tether</option>
                </select>
            </label>
        <Link to="/Contact">Contact</Link>
    </div>
    );
};
