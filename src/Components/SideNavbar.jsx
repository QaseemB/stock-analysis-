import React, { useState } from 'react'


export const SideNav = (props) => {
    const [collapsed, setCollapsed] = useState(false);
    function handleToggleSidebar() {
    setCollapsed(!collapsed);
}
return (
    <div className={`sideNav ${collapsed ? 'collapsed' : ''}`}>
        <button onClick={handleToggleSidebar}>Toggle sidebar</button>
        <a href="test1">Stocks</a>
        <a href="test2">Crypto</a>
        <a href="#">Contact</a>
    </div>
    );
};
