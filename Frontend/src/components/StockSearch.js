import React, { Component } from "react";
import Select from "react-select"


function convertToSelectOptions(data) {
    let assets = data.bestMatches;
    var arr = [];

    if (data && assets.length > 0) {
        for (let index = 0; index < assets.length; index++) {
            const assetName = assets[index]["2. name"]
            let shouldAppend = true;

            for (let i = 0; i < arr.length; i++) {
                if (assetName === arr[i].label) {
                    shouldAppend = false;
                }
            }

            if (shouldAppend) {
                arr.push({ label: assetName, value: assets[index]["1. symbol"] });
            }
        }
    }

    return arr;
}

export default class StockSearch extends Component {

    constructor(props) {
        super(props);

        this.state = {
            filterText: "",
            options: [{}]
        }

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSelectStock = this.handleSelectStock.bind(this);
    }

    fetchFromApi(SYMBOL_SEARCH) {
        const API_KEY = "G9O7IC9NDTXA3USU";
        fetch(`https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=${SYMBOL_SEARCH}&apikey=${API_KEY}`)
            .then(res => res.json())
            .then(response => this.processResponse(response))
            .catch(error => alert(error));
    }

    processResponse(response) {
        this.setState({ options: convertToSelectOptions(response) });
    }

    handleSelectStock(userSelect) {
        this.props.onSelectStock(userSelect);
    }

    handleInputChange(filterText) {

        this.setState({ filterText: filterText });

        if (filterText.length >= 3) {
            this.fetchFromApi(filterText);
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
                        options={this.state.options}
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