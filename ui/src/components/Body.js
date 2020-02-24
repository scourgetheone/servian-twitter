import React, { Component } from "react";

class Body extends Component {
  constructor() {
    super();

    this.state = {
        value: ""
    };

  }

  render() {
    return (
        <div>Hello, world</div>
    );
  }
}

export default Body;
