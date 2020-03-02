import Body from "./components/Body";
import React from "react";
import ReactDOM from "react-dom";

// Get the div element with id="container" and render the Body component there
const wrapper = document.getElementById("container");
wrapper ? ReactDOM.render(<Body />, wrapper) : false;
