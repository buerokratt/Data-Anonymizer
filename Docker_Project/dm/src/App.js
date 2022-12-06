import "./App.css";
import "antd/dist/antd.css";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Anonymizer from "./components/Anonymizer";
import Treening from "./components/Treening";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Anonymizer />} />
        <Route path="/treening" element={<Treening />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
