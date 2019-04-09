import {Component} from "react";
import React from "react";
import { Calendar, Alert , Table, Button, Radio, message} from 'antd';
import * as moment from 'moment';
import {Modal, FormGroup, FormControl, ControlLabel, Alert as ReactAlert} from 'react-bootstrap';
import { fetchAPI } from '../../utility'
import 'antd/es/calendar/style/index.css';
import 'antd/es/alert/style/index.css';
import 'antd/es/table/style/index.css';
import 'antd/es/divider/style/index.css';
import 'antd/es/button/style/index.css';
import 'antd/es/select/style/index.css';
import 'antd/es/pagination/style/index.css';
import 'antd/es/icon/style/index.css';
import 'antd/es/tabs/style/index.css';
import 'antd/es/radio/style/index.css';
import 'antd/es/typography/style/index.css';
import 'antd/es/message/style/index.css';

class BookDoctor extends Component {
    constructor(props) {
        super(props);
        var update = require('react-addons-update');
        this.state = {
            size : 'checkin',
            current : moment(),
            value: moment(),
            selectedValue: moment(),
            timeSlots: ['8:00', '8:20', '8:40', '9:00', '9:20', '9:40', '10:00', '10:20', '10:40', '11:00', '11:20', '11:40','12:00', '12:20', '12:40','13:00', '13:20', '13:40','14:00', '14:20', '14:40','15:00', '15:20', '15:40','16:00', '16:20', '16:40','17:00', '17:20', '17:40','18:00', '18:20', '18:40','19:00', '19:20', '19:40', '20:00'],
            availableTimeSlots: [],
            clinic: '',
            display1: [], //for checkups
            display2: [], //for annuals
            appointment: [], 
            modal: false,
            hcnumber: '',
            inexistentPatient: false,
            fail: false,
            noRoom: false,
            patientAlreadyBooked: false
        }
    }
    
    componentDidMount(){
        this.getTimeSlots(moment())
    }

    componentWillReceiveProps(nextProps) {
        if(this.props !== nextProps){
          this.getTimeSlots(this.state.selectedValue)
        }
    }

    onSelect = (value) => {
        this.setState({
        value,
        selectedValue: value,
        });
        this.getTimeSlots(value)
    }

    onChange = (e) => {
        this.setState({ size: e.target.value });
    }

    onPanelChange = (value) => {
        this.setState({ value });
    }

    handleBooking = (e) => {
        this.bookAppointment()
    }

    handleOpenModal = (app) => {
        this.setState({appointment: app, modal: true})
    }

    handleCloseModal = (e) => {
        this.setState({appointment: '', modal: false})
    }

    handleChange = event => {
        this.setState({
          [event.target.id]: event.target.value
        }, ()=>{});
    }

    getAvails(schedule){
        let avails = [];
        for (let i=0; i<35; i++) {
            avails.push(schedule[i].split(':')[2])
            avails[i] = (avails[i] == 'true') // convert from string to boolean
        }
        this.setState({availableTimeSlots: avails})
    }

    async getTimeSlots(date) {
        let data = {date: date.format('YYYY-MM-DD') }
        fetchAPI("GET", "/api/nurse/doctorAvailability?permit_number=" + this.props.user.permit_number +
            "&access_ID=" + this.props.access_ID + 
            "&password_hash=" + this.props.password_hash +
            "&date=" + data.date).then(
                response => {
                    try{
                        if (response.success){
                            console.log('it is a success mate')
                            this.getAvails(response.schedule)
                            let data1 = [] //for checkups
                            let data2 = [] //for annuals
                            for (let i = 0; i<35; i++){
                                if (this.state.availableTimeSlots[i])
                                    data1.push({
                                        time: this.state.timeSlots[i] + " - " + this.state.timeSlots[i+1],
                                        button: <Button type="primary" icon="plus" size="large" onClick={() => 
                                            this.handleOpenModal(['Checkup', data.date, this.state.timeSlots[i]])}>BOOK</Button>
                                    })
                                if (this.state.availableTimeSlots[i] && this.state.availableTimeSlots[i+1] && this.state.availableTimeSlots[i+2] && i<=33)
                                    data2.push({
                                        time: this.state.timeSlots[i] + " - " + this.state.timeSlots[i+3],
                                        button: <Button type="primary" icon="plus" size="large" onClick={() => 
                                            this.handleOpenModal(['Annual', data.date, this.state.timeSlots[i]])}>BOOK</Button>
                                    })
                            }
                            this.setState({display1: data1, display2:data2, 
                                clinic: response.clinics[0], availableTimeSlots: []})
                        }
                        else {
                        console.log('it is a fail mate' + response.message);
                        }
                    } catch(e){console.error("Error", e)}
                }
            ).catch((e)=>console.error("Error:", e))
    }

    async bookAppointment() {
        let appointment = {hcnumber: this.state.hcnumber, permit_number: this.props.user.permit_number, 
            date: this.state.appointment[1], time: this.state.appointment[2], appointment_type: this.state.appointment[0],
                clinic_id: this.state.clinic.split(';')[0] }
        fetchAPI("POST", "/api/appointment/book/doctor", appointment).then(
                response => {
                    try{
                        if (response.success){
                            console.log('it is a success mate')
                            this.setState({inexistentPatient: false, modal: false, fail: false})
                            message.info(this.state.appointment[0] + " with " + this.state.hcnumber + " at " + 
                                this.state.appointment[2] + " on " + this.state.appointment[1] + " at " +  
                                this.state.clinic.split(';')[1] + " has been booked.")
                            this.getTimeSlots(this.state.selectedValue)
                            this.props.handleUpdate()
                        }
                        else {
                            console.log('it is a fail mate ' + response.message);
                            if (!response.patientExists)
                                this.setState({inexistentPatient: true})
                            else
                                this.setState({fail: true})
                        }
                    } catch(e){console.error("Error", e)}
                }
            ).catch((e)=>console.error("Error:", e))
    }

    render() {
        const { current, value, selectedValue, size } = this.state;
        let message, success, patientAlert, alert, roomAlert, patientAlreadyBookedAlert;

        if (selectedValue < current) {
            message = "You cannot select a previous date to book an appointment";
            success = false;
        } else
        {
            message = "You selected date: " + selectedValue.format('YYYY-MM-DD');
            success = true;
        }

        if (this.state.inexistentPatient)
            patientAlert = <div className="flash animated" id="welcome"><ReactAlert bsStyle="warning">Patient does not exist.</ReactAlert></div>
        else
            patientAlert = null

        if (this.state.fail)
            alert = <div className="flash animated" id="welcome"><ReactAlert bsStyle="warning">Cannot book appointment.
                &nbsp; Check that your timeslot is still available.</ReactAlert></div>
        else
            alert = null

        if (this.state.noRoom)
            roomAlert = <div className="flash animated" id="welcome"><ReactAlert bsStyle="warning">No room available at that time.</ReactAlert></div>
        else
            roomAlert = null
        
        if (this.state.patientAlreadyBooked)
            patientAlreadyBookedAlert = <div className="flash animated" id="welcome"><ReactAlert bsStyle="warning">Patient already booked at this time and date.</ReactAlert></div>
        else
        patientAlreadyBookedAlert = null

        return (
            <div>
                <Modal show={this.state.modal}>
                        <Modal.Header>
                            <Modal.Title>Book {this.state.appointment[0]} appointment at {this.state.appointment[2]} on
                                &nbsp;{this.state.appointment[1]} at {this.state.clinic.split(';')[1]}
                                &nbsp; (clinic id: {this.state.clinic.split(';')[0]}).
                            </Modal.Title>
                        </Modal.Header>
                        <Modal.Body>
                            <form>
                                <FormGroup controlId="hcnumber" bsSize="large">
                                    <ControlLabel>Enter Patient's Health Card Number</ControlLabel>
                                    <FormControl
                                        autoFocus
                                        type="text"
                                        value={this.state.hcnumber}
                                        onChange={this.handleChange}
                                    />
                                </FormGroup>
                            </form>
                            {patientAlert}
                            {alert}
                            {roomAlert}
                            {patientAlreadyBookedAlert}
                        </Modal.Body>
                        <Modal.Footer>
                            <Button variant="secondary" onClick={this.handleCloseModal}>Cancel</Button>
                            <Button variant="primary" onClick={this.handleBooking}>Book</Button>
                        </Modal.Footer>
                </Modal>
                <table>
                    <tr>
                        <td colSpan={2}>
                            Select the type of appointment you want to book.
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <Radio.Group value={size} onChange={this.onChange} style={{ marginBottom: 16 }}>
                                <Radio.Button value="checkin">Check-In</Radio.Button>
                                <Radio.Button value="annual">Annual</Radio.Button>
                            </Radio.Group>
                        </td>
                    </tr>
                    <tr><td><Alert message={message}/></td></tr>
                    <tr>
                        <td><div><Calendar style={{width:300, height:200}} value={value} fullscreen={false}  onSelect={this.onSelect} onPanelChange={this.onPanelChange}/></div></td>
                        <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
                        <td style={{width:'100%'}}><AppointmentTable success={success} value={selectedValue} size={size} display1={this.state.display1} 
                        display2={this.state.display2} clinic={this.state.clinic}/></td>
                    </tr>
                </table>
            </div>
        );
    }
}

function AppointmentTable(props) {

    const columns = [{
      title: 'Time',
      dataIndex: 'time',
    }, {
      dataIndex: "button"
    }];


    if (!props.success) {
        return null;
    }
    else if (props.size == 'checkin') {
        return (
            <div>
                <h2>Available Appointments for {props.value.format('YYYY-MM-DD')}, at {props.clinic.split(';')[1]}
                &nbsp; (clinic id: {props.clinic.split(';')[0]})</h2>
                <Table columns={columns} dataSource={props.display1} pagination={false}/>
            </div>
        );
    }
    else if (props.size == 'annual') {
        return (
            <div>
                <h2>Available Appointments for {props.value.format('YYYY-MM-DD')}, at {props.clinic.split(';')[1]}
                &nbsp; (clinic id: {props.clinic.split(';')[0]})</h2>
                <Table columns={columns} dataSource={props.display2} pagination={false}/>
            </div>
        );
    }
}

export default BookDoctor;