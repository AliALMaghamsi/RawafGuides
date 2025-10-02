import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import {BrowserRouter as Router, Route, Routes, BrowserRouter} from 'react-router-dom'
import GuidesPage from './GuidesPage.jsx'
import LoginPage from './LoginPage.jsx'
import { Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
    
    <Routes>
      <Route path="/" element={<LoginPage/>}/>
      <Route path="/guides" element={<GuidesPage/>}/>
    </Routes>
    </BrowserRouter>
  )
}

export default App