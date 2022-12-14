import React, { useState, useEffect } from "react";
import StockSearchBar from "../components/StockSearchBar";
import MyDateRange from "../components/MyDateRange";
import { useNavigate } from "react-router-dom";
import "../styles/App.css";

const styleWaitingInfo = {
	color: "white",
	backgroundColor: "DodgerBlue",
	padding: "10px",
	fontFamily: "Arial",
	textAlign: "center"
};

function rfc3339(d) {

	function pad(n) {
		return n < 10 ? "0" + n : n;
	}

	function timezoneOffset(offset) {
		var sign;
		if (offset === 0) {
			return "Z";
		}
		sign = (offset > 0) ? "-" : "+";
		offset = Math.abs(offset);
		return sign + pad(Math.floor(offset / 60)) + ":" + pad(offset % 60);
	}

	return d.getFullYear() + "-" +
		pad(d.getMonth() + 1) + "-" +
		pad(d.getDate()) + "T" +
		pad(d.getHours()) + ":" +
		pad(d.getMinutes()) + ":" +
		pad(d.getSeconds()) +
		timezoneOffset(d.getTimezoneOffset());
}

function convertToSelectOptions(data) {
	let assets = data.assets_names;
	var arr = [];

	if (data && assets.length > 0) {
		for (let index = 0; index < assets.length; index++) {
			if (assets[index].token !== undefined) {
				arr.push({ label: assets[index].token, value: assets[index].token });
			}
		}
	}

	return arr;
}

function retriveDateRangeForToken(assets, token) {

	for (let index = 0; index < assets.length; index++) {
		if (assets[index].token === token) {
			let startTime = new Date(Date.parse(assets[index].start_date));
			let endTime = new Date(Date.parse(assets[index].end_date));
			return { startTime: startTime, endTime: endTime };
		}
	}

	return { start_date: Date.now(), end_date: Date.now() };
}

function checkIfDateRangeValid(dateRange, validDateRange) {
	if (dateRange.startTime < validDateRange.startTime ||
		dateRange.endTime > validDateRange.endTime) {
		return false;
	}

	return true;
}

async function requestModelOutput(endpoint, params) {
	let responseWithTwitter;
	let responseWithoutTwitter;

	params.is_twitter = true;
	await makeFetch(endpoint, params)
		.then(response => responseWithTwitter = response)
		.catch("error");

	params.is_twitter = false;
	await makeFetch(endpoint, params)
		.then(response => responseWithoutTwitter = response)
		.catch("error");

	let state =
	{
		responseWithTwitter: responseWithTwitter,
		responseWithoutTwitter: responseWithoutTwitter
	};

	return state;
}

function makeFetch(endpoint, params) {

	const requestOptions = {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(params)
	};

	let result = fetch(endpoint, requestOptions)
		.then(response => response.json())
		.catch(err => alert("There was an error:" + err));

	return result;
}

export default function NNModelForm() {

	const endpoint = "/train";
	const [userChosenToken, setToken] = useState("");
	const [isTokenValid, setTokenValid] = useState(true);
	const [areNNParamsValid, setAreNNParamsValid] = useState(true);
	const [companyName, setTokenCompanyName] = useState("");
	const [dateRange, setDateRange] = useState({ startTime: new Date(), endTime: new Date() });
	const [validDateRange, setValidDateRange] = useState({ startTime: new Date(), endTime: new Date() });
	const [assets, setAssets] = useState(null);
	const [assetsSelectList, setAssetsSelectList] = useState(null);
	const [isDateRangeValid, setIsDateRangeValid] = useState(true);

	const [shouldDisplayWaitingElement, setShouldDisplayWaitingElement] = useState(false);

	useEffect(() => {
		function fetchData() {
			fetch("/assets")
				.then(res => res.json())
				.then(response => processResponse(response))
				.catch(error => console.log(error));
		}
		fetchData();
	}, []);

	function processResponse(response) {
		setAssetsSelectList(convertToSelectOptions(response));
		setAssets(response.assets_names);
	}

	const navigate = useNavigate();

	const handleSelectStock = (userSelect) => {
		setToken(userSelect.value);
		setTokenValid(true);
		setTokenCompanyName(userSelect.label);
		const initialValidDateRange = retriveDateRangeForToken(assets, userSelect.value);
		setValidDateRange(initialValidDateRange);
		setDateRange(initialValidDateRange);
		console.log(validDateRange);
	}

	const handleDateRangeChange = (dateRange) => {
		setDateRange(dateRange);

		if (dateRange.startTime > dateRange.endTime ||
			!checkIfDateRangeValid(dateRange, validDateRange)) {
			setIsDateRangeValid(false);
		}
		else {
			setIsDateRangeValid(true);
		}
	}

	const AreFormFieldValid = (nnParams) => {

		var valid = true;

		if (userChosenToken.length === 0) {
			setTokenValid(false);
			return false;
		}
		else {
			setTokenValid(true);
		}

		for (let index = 0; index < nnParams.length; index++) {

			const param = nnParams[index];

			if (param !== undefined) {
				if ((param.value.trim().length > 0)) {
					setAreNNParamsValid(true);
				}
				else {
					setAreNNParamsValid(false);
					valid = false;

					return false;
				}
			}
			else {
				setAreNNParamsValid(false);
				valid = false;
				return false;
			}
		}

		if (!isDateRangeValid) {
			valid = false;
		}

		return valid;
	}

	async function handleSubmit(event) {

		event.preventDefault();

		var nrOfLayers = event.target.nrOfLayers;
		var learningRate = event.target.learningRate;
		var nrOfHiddenDimensions = event.target.nrOfHiddenDimensions;
		var lookBack = event.target.lookBack;
		var batchSize = event.target.batchSize;

		var nnParams = [nrOfLayers, learningRate, nrOfHiddenDimensions, lookBack, batchSize];

		if (AreFormFieldValid(nnParams)) {
			var params = {
				token: userChosenToken,
				start_date: rfc3339(dateRange.startTime),
				end_date: rfc3339(dateRange.endTime),
				number_of_layers: nrOfLayers.value,
				hidden_dim: nrOfHiddenDimensions.value,
				learning_rate: learningRate.value,
				look_back: lookBack.value,
				batch_size: batchSize.value
			}

			setShouldDisplayWaitingElement(true);

			requestModelOutput(endpoint, params)
				.then(state => navigate("/nnModelOutput", { state }));
		}
		else {
			alert("Parameters are invalid!");
		}
	}

	return (
		<>

			{shouldDisplayWaitingElement ? <div style={styleWaitingInfo}>Wait for response approx. 30 sec.</div> : <></>}

			<form id="stock_form" onSubmit={handleSubmit}>

				<label><i>Choose request params</i></label>
				<hr></hr>

				<StockSearchBar
					chosenCompanyName={companyName}
					onSelectStock={handleSelectStock}
					isTokenValid={isTokenValid}
					assetsSelectList={assetsSelectList}
				/>

				<MyDateRange
					onDateRangeChange={handleDateRangeChange}
					isDateRangeValid={isDateRangeValid}
					validDateRange={validDateRange}
				/>

				<label><i>Choose NN params</i></label>
				<hr></hr>

				<div className="div_for_my_label"><label className="my_label">Choose nr of layers</label> </div>
				<input name="nrOfLayers" type="number" min="1" defaultValue="1"></input>

				<div className="div_for_my_label"><label className="my_label">Choose learning rate</label> </div>
				<input name="learningRate" type="number" min="0" max="1" step="0.00001" defaultValue="0.0008"></input>

				<div className="div_for_my_label"><label className="my_label">Choose nr hidden dimensions</label> </div>
				<input name="nrOfHiddenDimensions" type="number" min="1" defaultValue="1"></input>

				<div className="div_for_my_label"><label className="my_label">Choose lookBack</label> </div>
				<input name="lookBack" type="number" min="1" defaultValue="5"></input>

				<div className="div_for_my_label"><label className="my_label">Choose batch size</label> </div>
				<input name="batchSize" type="number" min="1" defaultValue="64"></input>

				{(!areNNParamsValid) ? <span style={{ color: "red" }}><div>Input correct NN params</div></span> : <></>}

				<div className="submit_input_div"><input type="submit" defaultValue="Send" /></div>

			</form>
		</>
	);
}