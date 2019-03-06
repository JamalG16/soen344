import {Component} from "react";
import React from "react";
import { Calendar, Alert , Table, Button, Tabs, Radio, Typography, Divider} from 'antd';
import * as moment from 'moment';
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

class CalendarDoctor extends Component {

    state = {
        current : moment(),
        value: moment(),
        selectedValue: moment(),
    }

    onSelect = (value) => {
        this.setState({
        value,
        selectedValue: value,
        });
    }

    onPanelChange = (value) => {
        this.setState({ value });
    }

    render() {
        const { current, value, selectedValue } = this.state;
        let message, success;

        if (selectedValue < current) {
            message = "You cannot select a previous date to book an appointment";
            success = false;
        } else
        {
            message = "You selected date: " + selectedValue.format('YYYY-MM-DD');
            success = true;
        }

        return (
            <table>
                <tr><td><Alert message={message}/></td></tr>
                <tr>
                    <td><div><Calendar style={{width:300, height:200}} value={value} fullscreen={false}  onSelect={this.onSelect} onPanelChange={this.onPanelChange}/></div></td>
                    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
                    <td style={{width:'100%'}}><AppointmentTable success={success} value={selectedValue}/></td>
                </tr>
            </table>
        );
    }

}

function AppointmentTable(props) {

    let temp = moment(props.value);
    let week = moment();

    switch (props.value.day()) {
        case 0:
            week = moment(temp)
            break;
        case 1:
             week = moment(temp.subtract(1,"days"))
            break;
        case 2:
            week = moment(temp.subtract(2,"days"))
           break;
        case 3:
            week = moment(temp.subtract(3,"days"))
           break;
        case 4:
            week = moment(temp.subtract(4,"days"))
           break;
        case 5:
            week = moment(temp.subtract(5,"days"))
           break;
        case 6:
            week = moment(temp.subtract(6,"days"))

    }

    const columns = [{
      title: 'Sunday ' + week.format('DD'),
      dataIndex: 'time',
    },
        {
      title: 'Monday '+ week.add(1, "days").format("DD"),
      dataIndex: 'time',
    },
    {
      title: 'Tuesday ' + week.add(1, "days").format("DD"),
      dataIndex: 'time',
    },
    {
      title: 'Wednesday '+ week.add(1, "days").format("DD"),
      dataIndex: 'time',
    },
    {
      title: 'Thursday '+ week.add(1, "days").format("DD"),
      dataIndex: 'time',
    },
    {
      title:'Friday '+ week.add(1, "days").format("DD"),
      dataIndex: 'time',
    },
    {
      title: 'Saturday '+ week.add(1, "days").format("DD"),
      dataIndex: 'time',
    }];

    const data =
        [{time: "8:00-8:20"},
            {time: "8:20-8:40"},
            {time: "8:40-9:00"},
            {time: "9:20-9:40"},
            {time: "9:40-10:00"},
            {time: "10:20-10:40"},
            {time: "10:40-11:00"},
            {time: "11:00-11:20"},
            {time: "11:20-11:40"},
            {time: "11:40-12:00"},
            {time: "12:00-12:30"},
            {time: "12:30-13:00"},
            {time: "13:00-13:20"},
            {time: "13:20-13:40"},
            {time: "13:40-14:00"},
            {time: "14:00-14:20"},
            {time: "14:20-14:40"},
            {time: "14:40-15:00"},
            {time: "15:00-15:20"},
            {time: "15:20-15:40"},
            {time: "15:40-16:00"},
            {time: "16:00-16:20"},
            {time: "16:20-16:40"},
            {time: "16:40-17:00"},
            {time: "17:00-17:20"},
            {time: "17:20-17:40"},
            {time: "17:40-18:00"},
            {time: "18:00-18:20"},
            {time: "18:20-18:40"},
            {time: "18:40-19:00"},
            {time: "19:00-19:20"},
            {time: "19:20-19:40"},
            {time: "19:40-20:00"}

    ];


    if (!props.success) {
        return null;
    }
    return (
        <div>
            <h2>Available Appointments for {props.value.format('YYYY-MM-DD')}</h2>
            <Table columns={columns} dataSource={data} pagination={false}/>
        </div>
    );
}

export default CalendarDoctor;