import {Component} from "react";
import React from "react";
import {Tab, Tabs, Button, FormControl, FormGroup, ControlLabel, Alert} from "react-bootstrap";
import {fetchAPI} from '../../utility'
import BookPatient from "./../nurse views/BookPatient"
import AppointmentsPatient from "../nurse views/AppointmentsPatient";
import BookDoctor from "./../nurse views/BookDoctor"
import AppointmentsDoctor from "../nurse views/AppointmentsDoctor";

class HomepageNurse extends Component {
    constructor(props){
        super(props)
        this.state = {
            permit_number: '',
            hcnumber: '',
            permit_number: '',
            alertPatient: false,
            alertDoctor: false,
            user: {permit_number: '', hcnumber: ''},
            update: false
        }
        this.handleUpdate = this.handleUpdate.bind(this)
    }

    handleUpdate() {
        this.setState({update: true})
        this.setState({update: false})
    }

    handleChange = event => {
        this.setState({
        [event.target.id]: event.target.value
        }, ()=>{});
    }

    handleGetPatient = (e) => {
        e.preventDefault();
        let patient = {hcnumber: this.state.hcnumber}
        this.verifyPatient(patient)
    }

    handleGetDoctor = (e) => {
        e.preventDefault();
        let doctor = {permit_number: this.state.permit_number}
        this.verifyDoctor(doctor)
    }

    async verifyPatient(patient){
        fetchAPI("POST", "/api/patient/find/", patient).then(
            response => {
              try{
                if (response.success){
                  console.log('it is a success mate')
                  this.setState({foundPatient: true, alertPatient: false, user: {hcnumber: this.state.hcnumber,
                    permit_number: this.state.permit_number}})
                }
                else {
                  console.log('it is a fail mate');
                  this.setState({foundPatient: false, alertPatient: true, user: {hcnumber: '', 
                    permit_number: this.state.permit_number}})
                }
              } catch(e){console.error("Error", e)}
            }
          ).catch((e)=>console.error("Error:", e))
    }

    async verifyDoctor(doctor){
        fetchAPI("POST", "/api/doctor/find/", doctor).then(
            response => {
              try{
                if (response.success){
                  console.log('it is a success mate')
                  this.setState({foundDoctor: true, alertDoctor: false, user: {permit_number: this.state.permit_number,
                    hcnumber: this.state.hcnumber}})
                }
                else {
                  console.log('it is a fail mate');
                  this.setState({foundDoctor: false, alertDoctor: true, user: {permit_number:'',
                    hcnumber: this.state.hcnumber}})
                }
              } catch(e){console.error("Error", e)}
            }
          ).catch((e)=>console.error("Error:", e))
    }

    render(){
        let alertDoctor, alertPatient, successPatient, successDoctor, doctorHomePage, patientHomePage, patientBooking, doctorBooking;

        if (this.state.alertPatient){
            alertPatient = <div className="flash animated" id="welcome"><Alert bsStyle="warning">Patient has not been found.</Alert></div>
        }
        else{
            alertPatient = null
        }
          
        if (this.state.alertDoctor){
            alertDoctor = <div className="flash animated" id="welcome"><Alert bsStyle="warning">Patient has not been found.</Alert></div>
        }
        else{
            alertDoctor = null
        }

        if (this.state.foundPatient){
            successPatient = <div className="flash animated" id="welcome"><Alert bsStyle="success">Patient has been found.</Alert></div>
            patientHomePage = <AppointmentsPatient user={this.state.user} update={this.state.update} handleUpdate={this.handleUpdate}></AppointmentsPatient>
            patientBooking = <BookPatient user={this.state.user} update={this.state.update} handleUpdate={this.handleUpdate}></BookPatient>
        }
        else{
            successPatient = null
        }

        if (this.state.foundDoctor){
            successDoctor = <div className="flash animated" id="welcome"><Alert bsStyle="success">Doctor has been found.</Alert></div>
            doctorHomePage = <AppointmentsDoctor user={this.state.user} update={this.state.update} handleUpdate={this.handleUpdate}
                access_ID={this.props.user.access_ID} password_hash={this.props.user.password_hash}></AppointmentsDoctor>
            doctorBooking = <BookDoctor user={this.state.user} update={this.state.update} handleUpdate={this.handleUpdate}
                access_ID={this.props.user.access_ID} password_hash={this.props.user.password_hash}></BookDoctor>
        }
        else{
            successDoctor = null
        }

       return (
           <div>
               <h2>Choose Patient or Doctor to Book, Edit, or Cancel an appointment</h2>
                <Tabs defaultActiveKey="patient" id="uncontrolled-tab-example">
                    <Tab eventKey="patient" title="Patient">
                        <form onSubmit={this.handleGetPatient}>
                            <FormGroup controlId="hcnumber" bsSize="large">
                                <ControlLabel>Patient's health card number</ControlLabel>
                                <FormControl
                                    type="text"
                                    placeholder="ex: LOUX 1111 1111"
                                    value={this.state.hcnumber}
                                    onChange={this.handleChange}
                                />
                            </FormGroup>
                            <Button
                                block
                                bsSize="large"
                                type="submit"
                            >
                                Find Patient
                            </Button>
                        </form>
                        {successPatient}
                        {alertPatient}
                        <Tabs defaultActiveLey="appointments">
                            <Tab eventKey="appointments" title="Appointments">
                               {patientHomePage} 
                            </Tab>
                            <Tab eventKey="book" title="Book">
                                {patientBooking}
                            </Tab>
                        </Tabs>
                    </Tab>
                    <Tab eventKey="doctor" title="Doctor">
                        <form onSubmit={this.handleGetDoctor}>
                            <FormGroup controlId="permit_number" bsSize="large">
                                <ControlLabel>Doctor's permit number</ControlLabel>
                                <FormControl
                                    type="text"
                                    placeholder="ex: 1234567"
                                    value={this.state.permit_number}
                                    onChange={this.handleChange}
                                />
                            </FormGroup>
                            <Button
                                block
                                bsSize="large"
                                type="submit"
                            >
                                Find Doctor
                            </Button>
                        </form>
                        {successDoctor}
                        {alertDoctor}
                        <Tabs defaultActiveLey="appointments">
                            <Tab eventKey="appointments" title="Appointments">
                                {doctorHomePage}
                            </Tab>
                            <Tab eventKey="book" title="Book">
                                {doctorBooking}
                            </Tab>
                        </Tabs>
                    </Tab>
                </Tabs>
            </div>
       );
    }
}

export default HomepageNurse;