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

  handleLogin = event => {
    event.preventDefault();
    let user = {hcnumber: this.state.credentials, password: this.state.password }
    this.authenticate(user);
  }

  async authenticate(user){
    fetchAPI("POST", "/api/patients/authenticate/", user).then(
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