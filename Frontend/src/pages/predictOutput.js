import React from "react";
import { useLocation } from "react-router-dom";
import "../styles/App.css";

const PredictOutput = () => {

    let location = useLocation();
    let roundedModelPrediction = "-";
    let token = "-";

    if (typeof location.state !== "undefined" && location.state !== null) {
        let modelPrediction = location.state.modelPrediction;
        roundedModelPrediction = Math.round((modelPrediction + Number.EPSILON) * 100) / 100;
        token = location.state.token;
    }

    let tomorrow = new Date();
    tomorrow.setDate((new Date()).getDate() + 1)

    return (
        <>
            <h3>Model prediction for {token + " for " + tomorrow.toLocaleDateString() + " (tomorrow)"}</h3>
            <h2>{roundedModelPrediction}$</h2>
        </>
    );
};

export default PredictOutput;