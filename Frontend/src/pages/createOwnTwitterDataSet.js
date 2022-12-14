import React, { useState } from "react";
import StockSearch from "../components/StockSearch.js";
import MyDateRange from "../components/MyDateRange.js";
import "../styles/App.css";

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

async function requestTwitterDataCreation(params, endpoint) {

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(params)
    };

    let result = await fetch(endpoint, requestOptions)
        .then(_ => alert("We will email you when process is finished :)"))
        .catch(error => alert(`There was an error: ${error}. Try again later.`));

    return result;
}

export default function CreateOwnTwitterDataSet() {

    //const SENTIMENTAL_ENGINE_URL = SetUrl("http://engine:6000", "127.0.0.1:6000");

    const [userChosenToken, setToken] = useState("");
    // wywal isTOkenValid
    const [isTokenValid, setIsTokenValid] = useState(true);
    const [companyName, setTokenCompanyName] = useState("");
    const [dateRange, setDateRange] = useState({ startTime: new Date(), endTime: new Date() });
    const [isDateRangeValid, setIsDateRangeValid] = useState(true);
    const [areParamsValid, setAreParamsValid] = useState(true);
    const [query, setQuery] = useState("");
    const [bearerToken, setBearerToken] = useState("");
    const [email, setEmail] = useState("");

    const validDateRange = { startTime: new Date(), endTime: new Date() };

    const handleSelectStock = (userSelect) => {
        setToken(userSelect.value);
        setIsTokenValid(true);
        setTokenCompanyName(userSelect.label);
    }

    const handleDateRangeChange = (dateRange) => {
        setDateRange(dateRange);

        if (dateRange.startTime > dateRange.endTime) {
            setIsDateRangeValid(false);
        }
        else {
            setIsDateRangeValid(true);
        }
    }

    const onQueryChange = (query) => {
        setQuery(query.target.value);
    }

    const onBearerTokenChange = (bearerToken) => {
        setBearerToken(bearerToken.target.value);
    }

    const onEmailChange = (email) => {
        setEmail(email.target.value);
    }

    const AreParamsValid = () => {
        if (userChosenToken.length === 0) {
            setIsTokenValid(false);
            return false;
        }
        else {
            setIsTokenValid(true);
        }

        if (!isDateRangeValid) {
            return false;
        }

        if (query.length === 0) {
            return false;
        }

        if (bearerToken.length === 0) {
            return false;
        }

        if (email.length === 0) {
            return false;
        }

        return true;
    }

    async function handleSubmit(event) {

        event.preventDefault();

        if (AreParamsValid()) {
            var params = {
                asset_name: companyName,
                token: userChosenToken,
                start_time: rfc3339(dateRange.startTime),
                end_time: rfc3339(dateRange.endTime),
                query: query,
                bearer_token: bearerToken,
                email: email
            }

            await requestTwitterDataCreation(params, "/user-scrap-tweets");

            setIsTokenValid(true);
            setTokenCompanyName("");
            setDateRange({ startTime: new Date(), endTime: new Date() });
            setIsDateRangeValid(true);
            setAreParamsValid(true);
            setQuery("");
            setBearerToken("");
        }
        else {
            setAreParamsValid(false);
        }
    }

    return (
        <>
            <form id="stock_form" onSubmit={handleSubmit}>

                <StockSearch
                    chosenCompanyName={companyName}
                    onSelectStock={handleSelectStock}
                    isTokenValid={isTokenValid}
                />

                <MyDateRange
                    onDateRangeChange={handleDateRangeChange}
                    isDateRangeValid={isDateRangeValid}
                    validDateRange={validDateRange}
                />

                <div className="div_for_my_label"><label className="my_label">Type in query to scrap chosen tweets</label> </div>
                <input name="queryText" type="text" onChange={onQueryChange}></input>

                <div className="div_for_my_label"><label className="my_label">Type in your twitter bearer token</label> </div>
                <input name="bearerToken" type="text" onChange={onBearerTokenChange}></input> {/* maybe add check if token is valid? */}

                <div className="div_for_my_label"><label className="my_label">Type in your email</label> </div>
                <input name="user_email" type="email" onChange={onEmailChange}></input>

                {(!areParamsValid) ? <span style={{ color: "red" }}><div>Incorrect params</div></span> : <></>}

                <div className="submit_input_div"><input type="submit" defaultValue="Send" /></div>

            </form>
        </>
    );
}