import "./App.css";
import "antd/dist/antd.css";
import Anonymizer from "./components/Anonymizer";
import Treening from "./components/Treening";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Anonymizer />} />
        <Route path="/treening" element={<Treening />} />
      </Routes>
    </Router>
  );
}

export default App;
