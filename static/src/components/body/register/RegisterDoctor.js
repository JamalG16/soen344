import React, { Component } from "react";
import { FormGroup, FormControl, ControlLabel, Button, Alert } from "react-bootstrap";
import { fetchAPI } from '../../utility'
import './register.css'

class RegisterDoctor extends Component {
    constructor(props) {
        super(props)
        this.state = {
            //form inputs
            permit_number: '',
            fname: '',
            lname: '',
            specialty: '',
            password: '',
            confirmPassword: '',
            city: '',

            //validators
            validPermitNumber: null,
            validPassword: null,

            //alert notifies if account already exists
            alert: false,
            success: false
        }
        this.validatePermitNumber = this.validatePermitNumber.bind(this)
        this.validatePassword = this.validatePassword.bind(this)
    }

    validateForm() {
        //check that all fields are valid
        return (this.state.fname.length>0 && this.state.lname.length>0 && this.state.validPermitNumber && 
            this.state.validPassword && this.state.specialty.length>0 && this.state.city.length>0)
    }

    handleChange = event => {
        this.setState({
        [event.target.id]: event.target.value
        });
    }

    validatePermitNumber(permit) {
        if (/^\d{7}$/.test(permit)){
            this.setState({validPermitNumber: true}, () => {})
        }
        else{
            this.setState({validPermitNumber: false}, () => {})
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
        let doctor = {
            permit_number: this.state.permit_number,
            fname: this.state.fname,
            lname: this.state.lname,
            specialty: this.state.specialty,
            password: this.state.password,
            city: this.state.city
            }
        this.register(doctor);
    }

    async register(doctor){
        fetchAPI("PUT", "/api/doctor/", doctor).then(
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
            permit_number: '',
            fname: '',
            lname: '',
            specialty: '',
            password: '',
            confirmPassword: '',
            city: '',

            //validators
            validPermitNumber: null,
            validPassword: null,
        })
    }

    render() {
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
                    <FormGroup controlId="permit_number" bsSize="large">
                        <ControlLabel>Permit Number</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="ex: 1234567"
                        value={this.state.permit_number}
                        onChange={(e) => {
                            this.validatePermitNumber(e.target.value)
                            this.setState({ permit_number: e.target.value })
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
                    <FormGroup controlId="city" bsSize="large">
                        <ControlLabel>City</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="Montreal"
                        value={this.state.city}
                        onChange={this.handleChange}
                        />
                    </FormGroup>
                    <FormGroup controlId="specialty" bsSize="large">
                        <ControlLabel>Specialty</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="Dermatologist"
                        value={this.state.specialty}
                        onChange={this.handleChange}
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

export default RegisterDoctor;