import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './components/Login'
import Home from './components/Home'
import GestionCajon from './components/GestionCajon'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/gestion-cajon/:cajonId" element={<GestionCajon />} />
      </Routes>
    </Router>
  )
}

export default App