import React, { Component } from "react";
import { Tabs, Tab} from "react-bootstrap";
import { connect } from 'react-redux'
import './register.css'
import RegisterPatient from './RegisterPatient'
import RegisterDoctor from './RegisterDoctor'
import RegisterNurse from './RegisterNurse'
import RegisterAdmin from "./RegisterAdmin";
import RegisterClinic from "./RegisterClinic";

class Register extends Component {
    render() {
        let display;

        //if admin, display the different registrations
        if (!(Object.keys(this.props.user).length === 0 && this.props.user.constructor === Object) && typeof(this.props.user.username) !== 'undefined')
            display = <div className="Register">
                <Tabs defaultActiveKey="patient" id="uncontrolled-tab-example">
                    <Tab eventKey="patient" title="Patient Registration">
                        <RegisterPatient></RegisterPatient>
                    </Tab>
                    <Tab eventKey="doctor" title="Doctor Registration">
                        <RegisterDoctor></RegisterDoctor>
                    </Tab>
                    <Tab eventKey="nurse" title="Nurse Registration">
                        <RegisterNurse></RegisterNurse>
                    </Tab>
                    <Tab eventKey="admin" title="Admin Registration">
                        <RegisterAdmin></RegisterAdmin>
                    </Tab>
                    <Tab eventKey="clinic" title="Clinic Registration">
                        <RegisterClinic></RegisterClinic>
                    </Tab>
                </Tabs>
            </div>
        //if any other type of user (patient, doc, nurse, visitor), then display regular patient registration
        else
            display = <div className="Register">
                    <Tabs defaultActiveKey="patient" id="uncontrolled-tab-example">
                        <Tab eventKey="patient" title="Patient Registration">
                            <RegisterPatient></RegisterPatient>
                        </Tab>
                    </Tabs>
                </div>
        return (
            <div>{display}</div>
        );
    }
}

function mapStateToProps(state) {
    return {
      user: state.login.user
    }
  }
  
  Register = connect(
    mapStateToProps,
  )(Register);
  
export default Register;