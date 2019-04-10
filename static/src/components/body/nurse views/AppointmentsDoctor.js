import {Component} from "react";
import React from "react";
import {Modal} from 'react-bootstrap';
import { Button, Alert } from 'react-bootstrap';
import {Card} from 'antd';
import 'antd/es/card/style/index.css';
import 'antd/es/modal/style/index.css';
import {fetchAPI} from "./../../utility";
import DoctorUpdateAppointment from './DoctorUpdateAppointment'

class AppointmentsDoctor extends Component {
 constructor(props) {
        super(props);
        this.state = {
            appointments:[],
            cardList:'',
            isLoading: true,
            modal: false,
            appointment: {},
            newAppointment: [],
            annualAlert: false,
            alert: false,
        };
        this.handleAppointmentsDoctor();
        this.cancel = this.cancel.bind(this)
    }

    componentWillReceiveProps(nextProps) {
        if(this.props !== nextProps){
          this.handleAppointmentsDoctor()
        }
    }

    handleOpenModal = (app) => {
        this.setState({appointment: app, modal: true})
    }

    handleCloseModal = (e) => {
        this.setState({appointmentId: '', modal: false})
    }

    handleSelect(newApp){
        this.setState({newAppointment: newApp})
    }

    handleUpdate = (e) => {
        this.updateAppointment()
    }

    async updateAppointment(){
        let data;
        if (this.state.newAppointment[0] == 'Checkup')
            data = {id: this.state.appointment.id, length:'20', permit_number: this.props.user.permit_number,
                time: this.state.newAppointment[2], date: this.state.newAppointment[1], 
                clinic_id: this.state.newAppointment[3].split(';')[0]}
        else
            data = {id: this.state.appointment.id, length:'60', permit_number: this.props.user.permit_number,
                time: this.state.newAppointment[2], date: this.state.newAppointment[1], 
                clinic_id: this.state.newAppointment[3].split(';')[0]}
        fetchAPI("PUT", '/api/appointment/update/doctor', data).then(
            response => {
                try{
                    if(response.success){
                        this.setState({
                            newAppointment: [], appointment:{}, modal: false, alert: false, annualAlert: false
                        });
                        console.log("Doctor successfully updated appointment with " + this.state.appointment.patient_hcnumber)
                        this.props.handleUpdate()
                    }
                    else {
                        console.log("Doctor unsuccessfully updated appointment with " + this.state.appointment.patient_hcnumber)
                        console.log(response.message)
                        if (response.bookableAnnual)
                            this.setState({alert: false, annualAlert: false})
                        else
                            this.setState({alert: false, annualAlert: true})
                    }
                    this.handleAppointmentsPatient();
                } catch(e) {console.error("Error getting appointments for patient:", e)}
            }
        ).catch((e)=>console.error("Error getting appointments for patient:", e))
    }

    async handleAppointmentsDoctor(){
        let route = "/api/appointment/checkDoctor?doctor_permit_number=" + this.props.user.permit_number;
           console.log(route);
           fetchAPI("GET",route).then(
               response => {
                   try{
                       if(response.success){
                           this.setState({
                               appointments: response.appointments
                           });
                           console.log("Doctor " + this.props.user.permit_number + " successfully retrieved appointments")
                       }
                       else {
                           console.log("Doctor " + this.props.user.permit_number + " failed to retrieve appointments")
                       }
                       this.generateCardList();
                   } catch(e) {console.error("Error getting appointments for Doctor:", e)}
               }
           ).catch((e)=>console.error("Error getting appointments for Doctor:", e))
       }

    async cancel(id){
        let data = {id: id}
        fetchAPI("DELETE", '/api/appointment/cancel', data).then(
            response => {
                try{
                    if(response.success){
                        this.setState({
                            appointments: response.appointments
                        });
                        console.log("Successfully cancelled appointment")
                        this.props.handleUpdate()
                    }
                    else {
                        console.log("Failed to cancel appointment")
                    }
                    this.handleAppointmentsDoctor();
                } catch(e) {console.error("Error getting appointments for doctor:", e)}
            }
        ).catch((e)=>console.error("Error getting appointments for doctor:", e))
    }

    async generateCardList() {
     let appointmentsAsCards = this.state.appointments.map((appointment) => {
         return (
             <div>
                 <Card
                    title={appointment.date}
                    extra={<div>
                            <a onClick={() => this.handleOpenModal(appointment)}>Update Appointment</a>
                            &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
                            <a onClick={() => this.cancel(appointment.id)}>Cancel Appointment</a>
                        </div>}
                    style={{ width: 800 }}>
                     <p>{appointment.length} minute appointment with patient: {appointment.patient_hcnumber}</p>
                     <p>Clinic id: {appointment.clinic_id}</p>
                     <p>Room: {appointment.room}</p>
                     <p>Time: {appointment.time}</p>
                </Card>
                <br/>
            </div>
         )
     });
     this.setState({cardList: appointmentsAsCards, isLoading: false})
    }

    render(){
        let alert, annualAlert;

        if (this.state.alert){
            alert = <div className="flash animated" id="welcome"><Alert bsStyle="warning">Appointment time is not available anymore.</Alert></div>
        }
        else{
            alert = null
        }

        if (this.state.annualAlert){
            annualAlert = <div className="flash animated" id="welcome"><Alert bsStyle="warning">It has not been a year since your last annual!</Alert></div>
        }
        else{
            annualAlert = null
        }
       return (
            <div>
                <br/>
                <br/>
                <br/>
                <Modal show={this.state.modal}>
                    <Modal.Header>
                        <Modal.Title>Select a New Appointment Date</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        {alert}
                        {annualAlert}
                        <DoctorUpdateAppointment access_ID={this.props.access_ID} password_hash={this.props.password_hash}
                        currentAppointment={this.state.appointment} handleSelect={this.handleSelect.bind(this)}></DoctorUpdateAppointment>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={this.handleCloseModal}>Cancel</Button>
                        <Button variant="primary" onClick={this.handleUpdate}>Update</Button>
                    </Modal.Footer>
                </Modal>
                <h3>Upcoming appointments:</h3>
                {this.state.isLoading ? 'Loading...' : this.state.cardList}
            </div>
       );
    }
}
export default AppointmentsDoctor;