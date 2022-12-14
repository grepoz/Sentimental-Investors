import React from "react";
import "../styles/navBar.css"

function Navbar() {
	return (
		<div className="navigation">
			<ul className="myUL">
				<li><a className="active" href="/about">About</a></li>
				<li><a href="/nnModelForm">Create own model</a></li>
				<li><a href="/predictAssetPrice">Predict</a></li>
				<li><a href="/createOwnTwitterDataSet">Create own data set</a></li>
			</ul>
		</div>
	);
}

export default Navbar;