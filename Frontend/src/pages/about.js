import React from "react";
import "../styles/App.css";

const About = () => {
	return (
		<div>
			<h1>Welcome to sentimental investors project!</h1>

			<article>
				<h1>What can you do with our app?</h1>

				<p>Our project enables you to predict tomorrows prices of choosen stock or cryptocurrency ie. Tesla, Bitcoin. </p>

				<p>Apart from that, you can create your own neural network model. Just select asset
					with date range and specify parameters for LSTM network.
				</p>
				<p>
					If you want to run predictions on your own data, which we currently don't support, feel free to use your
					twitter bearer token and download tweets, which we process for you.
				</p>
			</article>

			<article>
				<h1>How it works?</h1>

				<p>We've gatherd data about financial assets such as stocks and cryptocurrencies from Twitter and Yahoo finance. After that, we train
					LSTM model and enable you to use it, to predict tomorrows asset price.
				</p>
			</article>

			<article>
				<h1>About authors</h1>
				<p>Jeremi and Greg are studying computer science at Gdansk University of Technology.</p>

			</article>
		</div>
	);
};

export default About;