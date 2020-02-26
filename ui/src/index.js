/* global document */
import Body from "./components/Body";
import React from "react";
import ReactDOM from "react-dom";

const wrapper = document.getElementById("container");
wrapper ? ReactDOM.render(<Body />, wrapper) : false;
