import {Component} from "react";
import React from "react";
import { Calendar, Alert , Select} from 'antd';
import * as moment from 'moment';
import 'antd/es/calendar/style/index.css';
import 'antd/es/alert/style/index.css';
import 'antd/es/select/style/index.css';

class CalendarPatient extends Component {

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
        let message;

        if (selectedValue < current) {
            message = "You cannot select a previous date to book an appointment";
        } else
        {
            message = "You selected date: " + selectedValue.format('YYYY-MM-DD');
        }

        return (
            <div>
                <Alert message={message}/>
                <Calendar value={value} onSelect={this.onSelect} onPanelChange={this.onPanelChange}/>
            </div>
        );
    }

}

export default CalendarPatient;