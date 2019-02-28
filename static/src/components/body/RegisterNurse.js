import React, { Component } from "react";
import { FormGroup, FormControl, ControlLabel, Button, Alert } from "react-bootstrap";
import { fetchAPI } from '../utility'
import './register.css'

class RegisterNurse extends Component {
    constructor(props) {
        super(props)
        this.state = {
            //form inputs
            access_ID: '',
            fname: '',
            lname: '',
            password: '',
            confirmPassword: '',

            //validators
            validAccessID: null,
            validPassword: null,

            //alert notifies if account already exists
            alert: false,
            success: false
        }
        this.validateAccessID = this.validateAccessID.bind(this)
        this.validatePassword = this.validatePassword.bind(this)
    }

    validateForm() {
        //check that all fields are valid
        return (this.state.fname.length>0 && this.state.lname.length>0 && this.state.validAccessID && 
            this.state.validPassword)
    }

    handleChange = event => {
        this.setState({
        [event.target.id]: event.target.value
        });
    }

    validateAccessID(id) {
        if (/^[A-Z]{3}\d{5}$/.test(id)){
            this.setState({validAccessID: true}, () => {})
        }
        else{
            this.setState({validAccessID: false}, () => {})
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
        let nurse = {
            access_ID: this.state.access_ID,
            fname: this.state.fname,
            lname: this.state.lname,
            password: this.state.password,
            }
        this.register(nurse);
    }

    async register(nurse){
        fetchAPI("PUT", "/api/nurse/", nurse).then(
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
            access_ID: '',
            fname: '',
            lname: '',
            password: '',
            confirmPassword: '',

            //validators
            validAccessID: null,
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
                    <FormGroup controlId="access_ID" bsSize="large">
                        <ControlLabel>Access ID</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="ex: DOL12345"
                        value={this.state.access_ID}
                        onChange={(e) => {
                            this.validateAccessID(e.target.value)
                            this.setState({ access_ID: e.target.value })
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

export default RegisterNurse;