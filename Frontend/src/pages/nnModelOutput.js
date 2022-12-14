import React from "react";
import { useLocation } from "react-router-dom";
import { LineChart, Line, CartesianGrid, Legend } from "recharts";
import "../styles/App.css";
import "../styles/nnModelOutput.css";

function AddIndexes(responseWithTwitterTrainLoss, responseWithoutTwitterTrainLoss) {
	let data = [];
	let d;
	var i = 0;
	while (true) {

		if (i < responseWithTwitterTrainLoss.length && i < responseWithoutTwitterTrainLoss.length) {
			d = {
				index: i,
				withTwitterLoss: responseWithTwitterTrainLoss[i],
				withoutTwitterLoss: responseWithoutTwitterTrainLoss[i]
			};
		}
		else if (i < responseWithTwitterTrainLoss.length) {
			d = {
				index: i,
				withTwitterLoss: responseWithTwitterTrainLoss[i]
			};
		}
		else if (i < responseWithoutTwitterTrainLoss.length) {
			d = {
				index: i,
				withoutTwitterLoss: responseWithoutTwitterTrainLoss[i]
			};
		}
		else {
			break;
		}

		data.push(d);
		i++;
	}

	return data;
}

const NNModelOutput = () => {

	let data = {};
	var location = useLocation();
	let responseWithTwitter = location.state.responseWithTwitter;
	let responseWithoutTwitter = location.state.responseWithoutTwitter;

	if (typeof responseWithTwitter !== "undefined" && responseWithTwitter !== null &&
		typeof responseWithoutTwitter !== "undefined" && responseWithoutTwitter !== null) {
		data = AddIndexes(responseWithTwitter.train_loss, responseWithoutTwitter.train_loss);
	}
	else {
		responseWithTwitter = { test_loss: "-" };
		responseWithoutTwitter = { test_loss: "-" };
	}

	// const tmpDate = [];
	// for (let i = 0; i < 100; i++) {
	// 	var d;
	// 	if (i > 50) {
	// 		d = {
	// 			index: i,
	// 			loss1: i * Math.sin(i),
	// 		};
	// 	}
	// 	else {
	// 		d = {
	// 			index: i,
	// 			loss1: i * Math.sin(i),
	// 			loss2: -i * Math.sin(i),
	// 		};
	// 	}

	// 	tmpDate.push(d);
	// }

	return (
		<>
			<div><h2>Model output</h2></div>

			<table style={{ width: "100%" }}>
				<thead>
					<tr>
						<th></th>
						<th>With twitter</th>
						<th>Without twitter</th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<th>Test loss</th>
						<td>{responseWithTwitter.test_loss}</td>
						<td>{responseWithoutTwitter.test_loss}</td>
					</tr>
				</tbody>
			</table>
			<div><h3>Train loss for both:</h3></div>
			<div className="chart">

				<LineChart
					width={960}
					height={600}
					data={data}
				>
					<CartesianGrid strokeDasharray="2 2" />
					<Line type="monotone" dataKey="withTwitterLoss" stroke="#eb3495" strokeWidth={3} dot={false} />
					<Line type="monotone" dataKey="withoutTwitterLoss" stroke="#3437eb" strokeWidth={3} dot={false} />
					<Legend />
				</LineChart>
			</div>
		</>
	);
};

export default NNModelOutput;