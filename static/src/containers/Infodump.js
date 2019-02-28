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
      lastAnnual: null
    }
    fetchAPI("PUT", "/api/patients/", patientData).then(
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

  async registerAdmin(){
    let adminData= { 
      username: 'admin',
      password: 'lol'
    }
    fetchAPI("PUT", "/api/admins/", adminData).then(
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

  render() {
    return (
      <div>
        
      </div>
    )
  }

}
export default infodump;

