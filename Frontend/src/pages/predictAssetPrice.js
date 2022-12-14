import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/App.css";
import "../styles/predictAssetPrice.css"

class Model {

	constructor(modelName) {

		var array = modelName.split("_");
		var params = adjustArray(array);

		this.token = params[0];
		this.startTime = params[1];
		this.endTime = params[2];
		this.nrOfLayers = params[3];
		this.learningRate = params[4];
		this.nrOfHiddenDimensions = params[5];
		this.lookBack = params[6];
		this.batchSize = params[7];
		this.isTwitter = params[8];
		this.modelName = modelName;
	}
}

function adjustArray(array) {
	array[8] = array[8].toLowerCase();

	return array;
}

function createJsonObjects(response) {

	var models = [];

	response.forEach(element => {
		var model = new Model(element);
		models.push(model);
	});

	return models;
}

const Prediction = () => {

	const [radioChoice, setRadioChoice] = useState({ modelName: "", radioValue: false, radioId: -1 });
	const [isRadioChosen, setIsRadioChosen] = useState(true);
	const [models, setModels] = useState([]);
	const navigate = useNavigate();

	useEffect(() => {
		function fetchData() {
			fetch("/models")
				.then(res => res.json())
				.then(response => setModels(createJsonObjects(response.model_names)))
				.catch(error => console.log(error));
		}
		fetchData();
	}, []);

	async function makeFetch() {

		const requestOptions = {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ model_name: radioChoice.modelName })
		};

		let response = await fetch("/predict", requestOptions)
			.then(response => response.json())
			.catch(err => alert("There was an error:" + err));

		return response;
	}

	async function handleSubmit(event) {

		event.preventDefault();

		if (radioChoice.radioId !== -1) {

			//alert(`Submitting prediction request for model: ${event.target[radioChoice.radioId].value}`);
			let response = await makeFetch();

			setIsRadioChosen(true);
			var chosenModel = new Model(radioChoice.modelName);
			let state = {
				modelPrediction: response.model_prediction,
				token: chosenModel.token
			};
			navigate("/predictOutput", { state });
		}
		else {
			setIsRadioChosen(false);
		}
	}

	return (
		<>
			<div>
				<form id="stock_form" onSubmit={handleSubmit}>

					<div className="div_for_my_label"><label className="my_label">Choose model</label></div>

					<div className="radio-options">
						{models.map((item, i) => (
							<div key={i}>
								<input
									type="radio"
									name="modelRadio"
									value={item.modelName}
									checked={radioChoice.radioValue === item.modelName}
									onChange={(e) => setRadioChoice({
										modelName: item.modelName,
										radioValue: e.target.value,
										radioId: i
									})}
									id={i}
								/>
								<label htmlFor={i}>{"token: " + item.token + ", start time: " + item.startTime + ", end time: " + item.endTime + ", hidden dim.: " + item.nrOfHiddenDimensions + ", lookback: " + item.lookBack + ", is twitter: " + item.isTwitter}</label>
							</div>
						))}
					</div>

					{(!isRadioChosen) ? <span style={{ color: "red" }}><div>Choose model!</div></span> : <></>}

					<div className="submit_input_div"><input type="submit" value="Predict" /></div>
				</form>
			</div>
		</>
	);
};

export default Prediction;