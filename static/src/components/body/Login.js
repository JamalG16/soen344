import React, { Component } from "react";
import { Button, FormGroup, FormControl, ControlLabel, Alert } from "react-bootstrap";
import { fetchAPI } from '../utility'
import { login } from '../../actions/auth'
import "./login.css";
import { connect } from 'react-redux'

class Login extends Component {
  constructor(props) {
    super(props);

    this.state = {
      credentials: "",
      password: "",
      hcnumber: "",
      alert: false,
      logged: false
    };
  }

  validateForm() {
    return this.state.credentials.length > 0 && this.state.password.length > 0;
  }

  handleChange = event => {
    this.setState({
      [event.target.id]: event.target.value
    });
  }

  //determines which kind of user is trying to log in and authenticates using the correct API. 
  handleLogin = event => {
    event.preventDefault();
    if (/^[A-Z]{4}\s\d{4}\s\d{4}$/.test(this.state.credentials))
        this.authenticatePatient();

    else if(/^\d{7}$/.test(this.state.credentials))
        this.authenticateDoctor();

    else if(/^[A-Z]{3}\d{5}$/.test(this.state.credentials))
        this.authenticateNurse();

    else
        this.authenticateAdmin();
  }

  async authenticatePatient(){
    let patient = {hcnumber: this.state.credentials, password: this.state.password }
    fetchAPI("POST", "/api/patient/authenticate/", patient).then(
      response => {
        try{
          if (response.success){
            login(response.user)
            console.log('it is a success mate, your info is ' + response.user.fname + response.user.hcnumber)
            this.setState({logged: true, alert: false})
          }
          else {
            console.log('it is a fail mate');
            this.setState({alert: true, logged: false})
          }
        } catch(e){console.error("Error", e)}
      }
    ).catch((e)=>console.error("Error:", e))
  }

  async authenticateDoctor(){
    let doctor = {permit_number: this.state.credentials, password: this.state.password }
    fetchAPI("POST", "/api/doctor/authenticate/", doctor).then(
      response => {
        try{
          if (response.success){
            login(response.user)
            console.log('it is a success mate, your info is ' + response.user.fname + response.user.permit_number)
            this.setState({logged: true, alert: false})
          }
          else {
            console.log('it is a fail mate');
            this.setState({alert: true, logged: false})
          }
        } catch(e){console.error("Error", e)}
      }
    ).catch((e)=>console.error("Error:", e))
  }

  async authenticateNurse(){
    let nurse = {access_ID: this.state.credentials, password: this.state.password }
    fetchAPI("POST", "/api/nurse/authenticate/", nurse).then(
      response => {
        try{
          if (response.success){
            login(response.user)
            console.log('it is a success mate, your info is ' + response.user.fname + response.user.access_ID)
            this.setState({logged: true, alert: false})
          }
          else {
            console.log('it is a fail mate');
            this.setState({alert: true, logged: false})
          }
        } catch(e){console.error("Error", e)}
      }
    ).catch((e)=>console.error("Error:", e))
  }

  async authenticateAdmin(){
    let admin = {username: this.state.credentials, password: this.state.password }
    fetchAPI("POST", "/api/admin/authenticate/", admin).then(
      response => {
        try{
          if (response.success){
            login(response.user)
            console.log('it is a success mate, your info is ' + response.user.username)
            this.setState({logged: true, alert: false})
          }
          else {
            console.log('it is a fail mate');
            this.setState({alert: true, logged: false})
          }
        } catch(e){console.error("Error", e)}
      }
    ).catch((e)=>console.error("Error:", e))
  }

  render() {
    let alert,logged = null
    if (this.state.alert){
      alert = <div className="flash animated" id="welcome"><Alert bsStyle="warning">Invalid credentials or password!</Alert></div>
    }
    else{
      alert = null
    } 

    if (this.state.logged){
      logged = <div className="flash animated" id="welcome"><Alert bsStyle="success">Succesfully logged in, redirecting...</Alert></div>
    }

    return (
      <div className="Login">
      {alert}
      {logged}
        <form onSubmit={this.handleLogin}>
          <FormGroup controlId="credentials" bsSize="large">
            <ControlLabel>Credentials</ControlLabel>
            <FormControl
              autoFocus
              type="text"
              value={this.state.credentials}
              onChange={this.handleChange}
            />
          </FormGroup>
          <FormGroup controlId="password" bsSize="large">
            <ControlLabel>Password</ControlLabel>
            <FormControl
              value={this.state.password}
              onChange={this.handleChange}
              type="password"
            />
          </FormGroup>
          <Button
            block
            bsSize="large"
            disabled={!this.validateForm()}
            type="submit"
          >
            Login
          </Button>
        </form>
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
    user: state.login.user
  }
}

Login = connect(
  mapStateToProps,
)(Login);

export default Login;