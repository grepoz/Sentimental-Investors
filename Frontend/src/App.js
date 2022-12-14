import React from "react";
import "./styles/App.css";
import Navbar from "./components/Navbar.js";
import { BrowserRouter as Router, Routes, Route }
    from "react-router-dom";
import Home from "./pages";
import About from "./pages/about.js";
import Prediction from "./pages/predictAssetPrice.js";
import NNModelOutput from "./pages/nnModelOutput.js";
import NNModelForm from "./pages/nnModelForm.js";
import PredictOutput from "./pages/predictOutput.js";
import CreateOwnTwitterDataSet from "./pages/createOwnTwitterDataSet.js";

function App() {

    return (
        <Router>
            <Navbar />
            <div id="main-container">
                <Routes>
                    <Route exact path="/" element={<Home />} />
                    <Route path="/about" element={<About />} />
                    <Route path="/predictAssetPrice" element={<Prediction />} />
                    <Route path="/nnModelForm" element={<NNModelForm />} />
                    <Route path="/nnModelOutput" element={<NNModelOutput />} />
                    <Route path="/predictOutput" element={<PredictOutput />} />
                    <Route path="/createOwnTwitterDataSet" element={<CreateOwnTwitterDataSet />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;