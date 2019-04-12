import React, {Component} from 'react'
import { Link } from 'react-router-dom'
import { logOut } from '../../actions/auth'
import {Icon} from 'antd';
import 'antd/es/icon/style/index.css';

class PatientMenu extends Component {
  
  render() {
    return (
        <div>
            Welcome {this.props.user.fname}!
            &nbsp;&nbsp;&nbsp;&nbsp;
            <Link to="/CalendarPatient">
                Book an Appointment
            </Link>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <Link to="/AppointmentCart">
                <Icon type="shopping-cart" /> Cart
            </Link>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <Link to="/Clinics">
                Clinics
            </Link>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <Link to="/Homepage" onClick={logOut}>
                Logout
            </Link>
        </div>
    );
  }
}


export default PatientMenu;
