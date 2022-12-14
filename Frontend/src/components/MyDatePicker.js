import React, { Component } from "react";
import DatePicker from "react-date-picker"

export default class MyDatePicker extends Component {

	currentDate = new Date();

	constructor(props) {
		super(props);
		this.state = {
			isDateValid: true
		}

		this.handleDateChange = this.handleDateChange.bind(this);
	}

	isDateValid = (date) => date !== null || date <= this.currentDate;

	handleDateChange(dateAsEvent) {
		this.props.onDateChange(dateAsEvent);
		this.setState({ isDateValid: this.isDateValid(dateAsEvent) });
	}

	render() {
		return (
			<>
				<div id="date_picker_div">
					<label>{this.props.labelBeforeDate}</label>
					<DatePicker
						value={this.props.date}
						onChange={this.handleDateChange}
					/>
					{(!this.state.isDateValid) ? <><br /><span style={{ color: "red" }}>Invalid date!</span></> : <></>}
				</div>
			</>
		)
	}
}