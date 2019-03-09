//Purpose of this class is to populate the db with some accounts. Used by developers
import React, { Component } from 'react';
import { fetchAPI } from '../components/utility'

class infodump extends Component {
  constructor(props) {
    super(props);
    this.state = ({
      sendDataAns: "no response so far" 
    })
  }

  /* 
   * This method is part of the lifecycle of a component in React.
   * If you want to know more about it, read the React Docs
   */
  componentDidMount() {
    this.registerPatient()
    this.registerAdmin()
    this.addRoom()
    this.addDoctor()
    this.addNurse()
  }

  /* 
  * sendData() is a blueprint for sending data to the db. 
  */

  async registerPatient(){
    let patientData= { 
      hcnumber: "LOUX 0803 2317",
      fname: "John",
      lname: "Doe", 
      birthday: "1995-10-10",
      gender: "M",
      phone: "4501234567",
      email: "johndoe@gmail.com", 
      address: "123 St. Catherine, Montreal QC",
      password: "lol", 
      lastAnnual: "2010-10-10"
    }
    fetchAPI("PUT", "/api/patient/", patientData).then(
        response => {
          try{
            if (response.success){
              console.log('it is a success mate')
              this.setState({sendDataAns: response.message})
            }
            else {
              console.log('it is a fail mate');
              this.book()
            }
          } catch(e){console.error("Error", e)}
        }
      ).catch((e)=>console.error("Error:", e))
  }

  async registerAdmin(){
    let adminData= { 
      username: 'admin',
      password: 'lol'
    }
    fetchAPI("PUT", "/api/admin/", adminData).then(
        response => {
          try{
            if (response.success){
              console.log('it is a success mate')
              this.setState({sendDataAns: response.message})
            }
            else {
              console.log('it is a fail mate');
            }
          } catch(e){console.error("Error", e)}
        }
      ).catch((e)=>console.error("Error:", e))
  }

  async addRoom(){
    let room= { 
      roomNumber: '10'
    }
    fetchAPI("PUT", "/api/room/", room).then(
        response => {
          try{
            if (response.success){
              console.log('it is a success mate')
              this.setState({sendDataAns: response.message})
            }
            else {
              console.log('it is a fail mate');
            }
          } catch(e){console.error("Error", e)}
        }
      ).catch((e)=>console.error("Error:", e))
  }
  async addDoctor(){
    let doctor= { 
      permit_number: '1234567',
      fname: "Jill",
      lname: "Doe",
      specialty: "Dermatologist",
      password: "lol",
      city: "Mtl"
    }
    fetchAPI("PUT", "/api/doctor/", doctor).then(
        response => {
          try{
            if (response.success){
              console.log('it is a success mate')
              this.setState({sendDataAns: response.message})
            }
            else {
              console.log('it is a fail mate');
            }
          } catch(e){console.error("Error", e)}
        }
      ).catch((e)=>console.error("Error:", e))
  }
  async addNurse(){
    let nurse= { 
      access_ID: 'ABC12345',
      fname: "Joseph",
      lname: "Doe",
      password: "lol",
    }
    fetchAPI("PUT", "/api/nurse/", nurse).then(
        response => {
          try{
            if (response.success){
              console.log('it is a success mate')
              this.setState({sendDataAns: response.message})
            }
            else {
              console.log('it is a fail mate');
            }
          } catch(e){console.error("Error", e)}
        }
      ).catch((e)=>console.error("Error:", e))
  }
  async book(){

    let appointment= { 
      hcnumber: 'LOUX 0803 2317',
      length: '20',
      time: '8:00',
      date: '2019-04-01'
    }
    fetchAPI("PUT", "/api/appointment/book", appointment).then(
        response => {
          try{
            if (response.success){
              console.log('it is a success matie!' + response.info)
              this.setState({sendDataAns: response.message})
            }
            else {
              console.log('it is a fail matie!');
              console.log(response.message + 'info:' +response.info)
            }
          } catch(e){console.error("Error", e)}
        }
      ).catch((e)=>console.error("Error:", e))
  }

  render() {
    return (
      <div>
        
      </div>
    )
  }

}
export default infodump;

