import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/HomePage"
import "@fontsource/montserrat";
import '@fortawesome/fontawesome-free/css/all.min.css';


function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  )
}

export default App
