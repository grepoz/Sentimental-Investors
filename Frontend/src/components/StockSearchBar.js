import React, { Component } from "react";
import Select from "react-select"

function filterOptions(assets, filterText) {

	var filteredOptions = [{}];

	for (let index = 0; index < assets.length; index++) {

		const asset = assets[index];

		var elementLowercase = asset.label.toLowerCase();
		var filterTextLowercase = filterText.toLowerCase();

		if (elementLowercase.indexOf(filterTextLowercase) !== -1) {
			filteredOptions.push(asset);
		}
	}

	return filteredOptions;
}

export default class StockSearchBar extends Component {

	constructor(props) {
		super(props);

		this.state = {
			filterText: "",
			displayedData: [{}]
		}

		this.handleInputChange = this.handleInputChange.bind(this);
		this.handleSelectStock = this.handleSelectStock.bind(this);
	}

	componentDidUpdate() {
		if (this.props.assetsSelectList !== undefined) {
			if (this.props.assetsSelectList !== this.state.displayedData) {
				this.setState({ displayedData: this.props.assetsSelectList });
			}
		}
	}

	handleSelectStock(userSelect) {
		this.props.onSelectStock(userSelect);
	}

	handleInputChange(filterText) {

		this.setState({ filterText: filterText })// filterText = "i"

		if (filterText.length > 0) {
			let filterData = filterOptions(this.state.displayedData, filterText);
			this.setState({ displayedData: filterData });
		}
		else {
			this.setState({ displayedData: this.props.assetsSelectList });
		}
	}

	render() {
		return (
			<>
				<div>
					<div className="div_for_my_label"><label className="my_label">Choose asset</label></div>

					<Select
						className="select_component"
						value={{ value: this.props.chosenCompanyName, label: this.props.chosenCompanyName }}
						options={this.state.displayedData}
						onChange={this.handleSelectStock}
						onInputChange={this.handleInputChange}
						placeholder={"Search..."}
					/>

					{(!this.props.isTokenValid) ? <span style={{ color: "red" }}><div>Choose asset!</div></span> : <></>}
				</div>
			</>
		)
	}
}