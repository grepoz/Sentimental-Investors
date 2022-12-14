import React, { Component } from "react";
import MyDatePicker from "./MyDatePicker";


export default class MyDateRange extends Component {

    currentDate = new Date();

    constructor(props) {
        super(props);
        this.state = {
            startTime: new Date(),
            endTime: new Date(),
            isStartTimeValid: true,
            isEndTimeValid: true,
            isDateRangeValid: true,
            componentInternalChange: false
        }

        this.handleStartTimeChange = this.handleStartTimeChange.bind(this);
        this.handleEndTimeChange = this.handleEndTimeChange.bind(this);
    }

    componentDidUpdate() {
        if (!this.state.componentInternalChange) {
            if (this.props.validDateRange.startTime !== undefined) {

                if (this.props.validDateRange.startTime !== this.state.startTime) {
                    this.setState({ startTime: this.props.validDateRange.startTime });
                }
            }

            if (this.props.validDateRange.endTime !== undefined) {
                if (this.props.validDateRange.endTime !== this.state.endTime) {
                    this.setState({ endTime: this.props.validDateRange.endTime });
                }
            }
        }
    }

    handleStartTimeChange(dateAsEvent) {
        this.setState({ startTime: dateAsEvent });

        if (dateAsEvent > this.currentDate || dateAsEvent === null) {
            this.setState({ isStartTimeValid: false });
        }
        else {
            this.setState({ isStartTimeValid: true });
            this.setState({ componentInternalChange: true });
            this.props.onDateRangeChange({ startTime: dateAsEvent, endTime: this.state.endTime })
        }
    }

    handleEndTimeChange(dateAsEvent) {
        this.setState({ endTime: dateAsEvent });

        if (dateAsEvent > this.currentDate || dateAsEvent === null) {
            this.setState({ isEndTimeValid: false });
        }
        else {
            this.setState({ isEndTimeValid: true });
            this.setState({ componentInternalChange: true });
            this.props.onDateRangeChange({ startTime: this.state.startTime, endTime: dateAsEvent });
        }
    }

    render() {//isDateValid = {this.state.isStartTimeValid} // isDateValid = {this.state.isUpperDateValid}
        return (
            <>
                <div className="div_for_my_label"><label className="my_label">Choose date</label> </div>
                <MyDatePicker
                    labelBeforeDate={"From: "}
                    date={this.state.startTime}
                    onDateChange={this.handleStartTimeChange}
                />

                <MyDatePicker
                    labelBeforeDate={"To: "}
                    date={this.state.endTime}
                    onDateChange={this.handleEndTimeChange}
                />
                {(!this.props.isDateRangeValid) ? <span style={{ color: "red" }}>Invalid date range! <br /></span> : <></>}
            </>
        )
    }
}