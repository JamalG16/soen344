import React, { Component } from "react";
import { FormGroup, FormControl, ControlLabel, Button, Alert } from "react-bootstrap";
import { fetchAPI } from '../utility'
import Select from 'react-select'
import './register.css'

class RegisterPatient extends Component {
    constructor(props) {
        super(props)
        this.state = {
            //form inputs
            hcnumber: '',
            fname: '',
            lname: '',
            birthday: '',
            gender: '',
            phone: '',
            email: '',
            address: '',
            password: '',
            confirmPassword: '',
            lastAnnual: '',

            //validators
            validHcNumber: null,
            validPhone: null,
            validEmail: null,
            validPassword: null,
            validBirthday: null,
            validLastAnnual: null,

            //alert notifies if account already exists
            alert: false,
            success: false
        }
        this.validateHcNumber = this.validateHcNumber.bind(this)
        this.validatePhone = this.validatePhone.bind(this)
        this.validateEmail = this.validateEmail.bind(this)
        this.validatePassword = this.validatePassword.bind(this)
        this.validateBirthday = this.validateBirthday.bind(this)
        this.validateLastAnnual = this.validateLastAnnual.bind(this)
        this.validateForm = this.validateForm.bind(this)

    }

    validateForm() {
        //check first if all info is valid and no last annual is entered OR all info is valid and last annual is valid
        return ((this.state.fname.length>0 && this.state.lname.length>0 && this.state.address.length>0 && this.state.validBirthday 
            && this.state.validHcNumber && this.state.validPhone && this.state.validEmail && this.state.validPassword 
            && (this.state.gender.value=='F' || this.state.gender.value=='M') && this.state.lastAnnual == "") || 
            (this.state.fname.length>0 && this.state.lname.length>0 && this.state.address.length>0 && this.state.validBirthday 
            && this.state.validHcNumber && this.state.validPhone && this.state.validEmail && this.state.validPassword 
            && (this.state.gender.value=='F' || this.state.gender.value=='M') && this.state.validLastAnnual))
    }

    handleChange = event => {
        this.setState({
        [event.target.id]: event.target.value
        });
    }

    validateHcNumber(hc) {
        if (/^[A-Z]{4}\s\d{4}\s\d{4}$/.test(hc)){
            this.setState({validHcNumber: true}, () => {})
        }
        else{
            this.setState({validHcNumber: false}, () => {})
        }
    }

    validateBirthday(bday){
        if (/^\d{4}-\d{2}-\d{2}$/.test(bday)){
            this.setState({validBirthday: true }, () => {})
        }
        else{
            this.setState({validBirthday: false}, () => {})
        }
    }

    validatePhone(phone){
        if (/^\d{3}\d{3}\d{4}$/.test(phone)){
            this.setState({validPhone: true }, () => {})
        }
        else{
            this.setState({validPhone: false}, () => {})
        }
    }

    validateEmail(email){
        if (/[^@]+@[^\.]+\..+/.test(email)){
            this.setState({validEmail: true }, () => {})
        }
        else{
            this.setState({validEmail: false}, () => {})
        }
    }

    validateLastAnnual(appt){
        if (/^\d{4}-\d{2}-\d{2}$/.test(appt)){
            this.setState({validLastAnnual: true }, () => {})
        }
        else{
            this.setState({validLastAnnual: false}, () => {})
        }
    }

    validatePassword(pass, confirmpass){
        if (pass == confirmpass  && pass.length>=6){
            this.setState({validPassword: true }, () => {})
        }
        else{
            this.setState({validPassword: false}, () => {})
        }
    }

    handleRegister = event => {
        event.preventDefault();
        if (this.state.validLastAnnual == false || this.state.validLastAnnual == null)
            this.setState({lastAnnual: null})
        let patient = {
            hcnumber: this.state.hcnumber,
            fname: this.state.fname,
            lname: this.state.lname,
            birthday: this.state.birthday,
            gender: this.state.gender.value,
            phone: this.state.phone,
            email: this.state.phone,
            address: this.state.address,
            password: this.state.password,
            lastAnnual: this.state.lastAnnual, 
            }
        this.register(patient);
    }

    async register(patient){
        fetchAPI("PUT", "/api/patient/", patient).then(
            response => {
              try{
                if (response.success){
                  console.log('it is a success mate')
                  this.setState({ alert: false, success: true})
                  this.reset();
                }
                else {
                  console.log('it is a fail mate');
                  this.setState({alert: true, success: false})
                }
              } catch(e){console.error("Error", e)}
            }
          ).catch((e)=>console.error("Error:", e))
    }

    reset() {
        this.setState({
            hcnumber: '',
            fname: '',
            lname: '',
            birthday: '',
            gender: '',
            phone: '',
            email: '',
            address: '',
            password: '',
            confirmPassword: '',
            lastAnnual: '',

            //validators
            validHcNumber: null,
            validPhone: null,
            validEmail: null,
            validPassword: null,
            validBirthday: null,
            validLastAnnual: null,
        })
    }

    render() {
        let genderOptions = [
            { value: 'M', label: 'Male' },
            { value: 'F', label: 'Female' },
        ];

        let alert, success;

        if (this.state.alert){
            alert = <div className="flash animated" id="welcome"><Alert bsStyle="warning">Account already exists!</Alert></div>
        }
        else{
            alert = null
        }
          
        if (this.state.success){
            success = <div className="flash animated" id="welcome"><Alert bsStyle="success">Account created!</Alert></div>
        }
        else{
            success = null
        }

        return (
            <div className="Register">
            {alert}
            {success}
                <form onSubmit={this.handleRegister}>
                    <FormGroup controlId="hcnumber" bsSize="large">
                        <ControlLabel>Health Card Number</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="ex: LOUX 0803 2317"
                        value={this.state.hcnumber}
                        onChange={(e) => {
                            this.validateHcNumber(e.target.value)
                            this.setState({ hcnumber: e.target.value })
                        }}
                        />
                    </FormGroup>
                    <FormGroup controlId="fname" bsSize="large">
                        <ControlLabel>First Name</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="John"
                        value={this.state.fname}
                        onChange={this.handleChange}
                        />
                    </FormGroup>
                    <FormGroup controlId="lname" bsSize="large">
                        <ControlLabel>Last Name</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="Doe"
                        value={this.state.lname}
                        onChange={this.handleChange}
                        />
                    </FormGroup>
                    <FormGroup controlId="birthday" bsSize="large">
                        <ControlLabel>Birthday</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="YYYY-MM-DD"
                        value={this.state.birthday}
                        onChange={(e) => {
                            this.validateBirthday(e.target.value)
                            this.setState({ birthday: e.target.value })
                        }}
                        />
                    </FormGroup>
                    <FormGroup controlId="gender" bsSize="large">
                        <ControlLabel>Gender</ControlLabel>
                        <Select
                            name="gender"
                            value={this.state.gender}
                            options={genderOptions}
                            onChange={(e) => {
                                if (e !== null) {
                                    this.setState({ gender: e }, () => {})
                                } else {
                                    this.setState({ gender: '' }, () => {})
                                }
                            }}
                        />
                    </FormGroup>
                    <FormGroup controlId="phone" bsSize="large">
                        <ControlLabel>Phone</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="ex: 4509999999"
                        value={this.state.phone}
                        onChange={(e) => {
                            this.validatePhone(e.target.value)
                            this.setState({ phone: e.target.value })
                        }}
                        />
                    </FormGroup>
                    <FormGroup controlId="email" bsSize="large">
                        <ControlLabel>Email</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="ex: johndoe@gmail.com"
                        value={this.state.email}
                        onChange={(e) => {
                            this.validateEmail(e.target.value)
                            this.setState({ email: e.target.value })
                        }}
                        />
                    </FormGroup>
                    <FormGroup controlId="address" bsSize="large">
                        <ControlLabel>Address</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="123 St-Catherine Street, Montreal, QC"
                        value={this.state.address}
                        onChange={this.handleChange}
                        />
                    </FormGroup>
                    <FormGroup controlId="lastAnnual" bsSize="large">
                        <ControlLabel>Last Annual Checkup</ControlLabel>
                        <FormControl
                        placeholder="Optional: YYYY-MM-DD"
                        value={this.state.lastAnnual}
                        onChange={(e) => {
                            this.validateLastAnnual(e.target.value)
                            this.setState({ lastAnnual: e.target.value })
                        }}
                        type="text"
                        />
                    </FormGroup>
                    <FormGroup controlId="password" bsSize="large">
                        <ControlLabel>Password</ControlLabel>
                        <FormControl
                        type="password"
                        placeholder="6 characters minimum"
                        value={this.state.password}
                        onChange={(e) => {
                            this.validatePassword(e.target.value, this.state.confirmPassword)
                            this.setState({ password: e.target.value })
                        }}
                        />
                    </FormGroup>
                    <FormGroup controlId="confirmPassword" bsSize="large">
                        <ControlLabel>Confirm Password</ControlLabel>
                        <FormControl
                        type="password"
                        placeholder="6 characters minimum"
                        value={this.state.confirmpassword}
                        onChange={(e) => {
                            this.validatePassword(this.state.password, e.target.value)
                            this.setState({ confirmPassword: e.target.value })
                        }}
                        />
                    </FormGroup>
                    <Button
                        block
                        bsSize="large"
                        disabled={!this.validateForm()}
                        type="submit"
                    >
                        Register
                    </Button>
                </form>
            </div>
        );
    }
}

export default RegisterPatient;