//Purpose of this class is to retrieve and dump information. Used by developers
import React, { Component } from 'react';

class infodump extends Component {
  constructor(props) {
    super(props);
    this.state = ({
      getDataAns: "no response so far",
      sendDataAns: "no response so far"
    })
  }

  /* 
   * This method is part of the lifecycle of a component in React.
   * If you want to know more about it, read the React Docs
   */
  componentDidMount() {
    this.getData()
    this.sendData()
  }

  /* 
  * getData() is a blueprint for fetching data from the db. 
  */
  async getData() {
    try {
      let myHeaders = new Headers();
      myHeaders.append('Content-Type', 'application/json');

      let myInit = {
        method: 'GET',
        headers: myHeaders
      };

      let req = new Request("/api/", myInit)
      let response = await fetch(req)

      let responseJson = await response.json()
      responseJson = JSON.stringify(responseJson)
      this.setState({getDataAns: responseJson})
    } catch (e) { console.error("Error: ", e) }
  }

  /* 
  * sendData() is a blueprint for sending data to the db. 
  */
  async sendData() {
    try {
      let data = { 
        hcnumber: "LOUX 0803 2317",
        fname: "John",
        lname: "Doe", 
        birthday: "10-10-1995",
        gender: "M",
        phone: "4501234567",
        email: "johndoe@gmail.com", 
        address: "123 St. Catherine, Montreal QC",
        password: "lol", 
        lastAnnual: null
      }

      let myHeaders = new Headers();
      myHeaders.append('Content-Type', 'application/json');
      let myInit = {
        method: 'PUT',
        body: JSON.stringify(data),
        headers: myHeaders
      };

      let req = new Request("/api/patients/", myInit)
      fetch(req).then(res => res.json())
      .catch(e => console.error('Error:', e))
      .then(response => {
        console.log(response)
        this.setState({sendDataAns:response.message})
      })
    } catch (e) { console.error("Error:", e) }
  }

  render() {
    return (
      <div>
        <p> getData: {this.state.getDataAns} </p>
        <p> </p>
        <p> sendData: {this.state.sendDataAns} </p>
      </div>
    )
  }

}
export default infodump;

