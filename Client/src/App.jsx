import { useState } from 'react'
import{SideNav} from './Components/SideNavbar';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import {Dashboard} from './Components/Dashboard';
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className='App'>
        <Router>
          <SideNav />
          <Dashboard />
        </Router>

      </div>
    </>
  )
}

export default App
