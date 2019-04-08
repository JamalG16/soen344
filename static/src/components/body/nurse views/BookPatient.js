import {Component} from "react";
import React from "react";
import { Calendar, Alert , Table, Button, Radio, message} from 'antd';
import * as moment from 'moment';
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

class BookPatient extends Component {
    constructor() {
        super();
        this.state = {
            size : 'checkin',
            current : moment(),
            value: moment(),
            selectedValue: moment(),
            timeSlots: ['8:00', '8:20', '8:40', '9:00', '9:20', '9:40', '10:00', '10:20', '10:40', '11:00', '11:20', '11:40','12:00', '12:20', '12:40','13:00', '13:20', '13:40','14:00', '14:20', '14:40','15:00', '15:20', '15:40','16:00', '16:20', '16:40','17:00', '17:20', '17:40','18:00', '18:20', '18:40','19:00', '19:20', '19:40', '20:00'],
            availableTimeSlots: [],
            display1: [], //for checkups
            display2: [], //for annuals
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

    async book(appointment){
        let booking;
        if (appointment[0] == 'Checkup')
            booking = {hcnumber: this.props.user.hcnumber, length: '20', time: appointment[2] , date: appointment[1] }
        else 
            booking = {hcnumber: this.props.user.hcnumber, length: '60', time: appointment[2] , date: appointment[1] }
        fetchAPI("PUT", "/api/appointment/book", booking).then(
            response => {
              try{
                if (response.success){
                    console.log('it is a success mate')
                    message.info('Booked a(n) ' + appointment[0] + ' appointment on ' + appointment[1] + ' at ' + appointment[2] + ' for ' + this.props.user.hcnumber + '.')
                    this.getTimeSlots(this.state.selectedValue)
                    this.props.handleUpdate()
                }
                else {
                  console.log('it is a fail mate' + response.message + response.info);
                  if (response.bookableAnnual){
                    message.info('Appointment time no longer exists.')
                    this.getTimeSlots(this.state.selectedValue)
                  }
                  else {
                    message.info('Could not book a(n) ' + appointment[0] + ' appointment on ' + appointment[1] + ' at ' + appointment[2] + ' for ' + this.props.user.hcnumber + '.' + 
                    ' It has not been a year since ' + this.props.user.hcnumber + '\'s last annual.')
                  }
                }
              } catch(e){console.error("Error", e)}
            }
          ).catch((e)=>console.error("Error:", e))
    }
    
    async getTimeSlots(date){
        let data = {date: date.format('YYYY-MM-DD') }
        fetchAPI("POST", "/api/appointment/find", data).then(
            response => {
              try{
                if (response.success){
                    console.log('it is a success mate')
                    this.setState({availableTimeSlots: response.listOfAvailableAppointments})
                    let data1 = [] //for checkups
                    let data2 = [] //for annuals
                    for (let i = 0; i<35; i++){
                        if (this.state.availableTimeSlots[i])
                            data1.push({
                                time: this.state.timeSlots[i] + " - " + this.state.timeSlots[i+1],
                                button: <Button type="primary" icon="plus" size="large" onClick={() => 
                                    this.book(['Checkup', data.date, this.state.timeSlots[i]])}>BOOK</Button>
                            })
                        if (this.state.availableTimeSlots[i] && this.state.availableTimeSlots[i+1] && this.state.availableTimeSlots[i+2] && i<=33)
                            data2.push({
                                time: this.state.timeSlots[i] + " - " + this.state.timeSlots[i+3],
                                button: <Button type="primary" icon="plus" size="large" onClick={() => 
                                    this.book(['Annual', data.date, this.state.timeSlots[i]])}>BOOK</Button>
                            })
                    }
                    this.setState({display1: data1, display2:data2})
                    this.setState({availableTimeSlots: []})
                }
                else {
                  console.log('it is a fail mate' + response.message);
                }
              } catch(e){console.error("Error", e)}
            }
          ).catch((e)=>console.error("Error:", e))
    }

    render() {
        const { current, value, selectedValue, size } = this.state;
        let message, success;

        if (selectedValue < current) {
            message = "You cannot select a previous date to book an appointment";
            success = false;
        } else
        {
            message = "You selected date: " + selectedValue.format('YYYY-MM-DD');
            success = true;
        }
        if (this.state.alert){
            alert = <div className="flash animated" id="welcome"><Alert bsStyle="warning">Appointment time is not available anymore.</Alert></div>
        }
        else{
            alert = null
        }

        return (
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
                    <td style={{width:'100%'}}><AppointmentTable success={success} value={selectedValue} size={size} display1={this.state.display1} display2={this.state.display2}/></td>
                </tr>
            </table>
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
                <h2>Available Appointments for {props.value.format('YYYY-MM-DD')}</h2>
                <Table columns={columns} dataSource={props.display1} pagination={false}/>
            </div>
        );
    }
    else if (props.size == 'annual') {
        return (
            <div>
                <h2>Available Appointments for {props.value.format('YYYY-MM-DD')}</h2>
                <Table columns={columns} dataSource={props.display2} pagination={false}/>
            </div>
        );
    }
}

export default BookPatient;