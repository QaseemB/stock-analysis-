import axios from 'axios';
import React, { useState, useEffect } from 'react';
import LinePlot from './LinePlot';


export function Dashboard() {
    return (
        <div>
            <h2>DashBoard</h2>
            <LinePlot data={[1,2,3,4,5]} />
        </div>
    )
}

export default {LinePlot}