const { createProxyMiddleware } = require("http-proxy-middleware");

let RNN_URL = "http://127.0.0.1:4000";
let ENGINE_URL = "http://127.0.0.1:5000";

if (!!(process.env.REACT_APP_DOCKERENV)) {
    RNN_URL = "http://rnn:4000";
    ENGINE_URL = "http://engine:5000";
}

const rnnProxyPOST = {
    target: RNN_URL,
    changeOrigin: true
}

const rnnProxyGET = {
    target: RNN_URL,
    changeOrigin: true,
    headers: {
        accept: "application/json",
        method: "GET",
    },
}

const engineProxy = {
    target: ENGINE_URL,
    changeOrigin: true
}

module.exports = function (app) {

    app.use(
        "/train",
        createProxyMiddleware(rnnProxyPOST)
    );

    app.use(
        "/predict",
        createProxyMiddleware(rnnProxyPOST)
    );

    app.use(
        "/assets",
        createProxyMiddleware(rnnProxyGET)
    );

    app.use(
        "/models",
        createProxyMiddleware(rnnProxyGET)
    );

    app.use(
        "/user-scrap-tweets",
        createProxyMiddleware(engineProxy)
    );
};
