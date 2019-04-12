import React, { Component } from "react";
import { FormGroup, FormControl, ControlLabel, Button, Alert } from "react-bootstrap";
import { fetchAPI } from '../../utility'
import './register.css'

class RegisterClinic extends Component {
    constructor(props) {
        super(props)
        this.state = {
            //form inputs
            name: '',
            address: '',
            rooms: '',

            //alert notifies if account already exists
            alert: false,
            success: false
        }
    }

    validateForm() {
        //check that all fields are valid
        return (this.state.name.length>0 && this.state.address.length>0 && /^\d+$/.test(this.state.rooms))
    }

    handleChange = event => {
        this.setState({
        [event.target.id]: event.target.value
        });
    }

    handleRegister = event => {
        event.preventDefault();
        let clinic = {
            name: this.state.name,
            address: this.state.address,
            }
        this.register(clinic);
    }

    async register(clinic){
        fetchAPI("PUT", "/api/clinic/", clinic).then(
            response => {
              try{
                if (response.success){
                  console.log('it is a success mate')
                  this.registerRooms(response.clinic.id)
                }
                else {
                  console.log('it is a fail mate');
                  this.setState({alert: true, success: false})
                }
              } catch(e){console.error("Error", e)}
            }
          ).catch((e)=>console.error("Error:", e))
    }

    async registerRooms(clinic_id){
        let room = {roomNumber: '', clinic_id: clinic_id}
        for (let i=1; i<=this.state.rooms; i++){
            room = {roomNumber: i, clinic_id: clinic_id}
            fetchAPI("PUT", "/api/room/", room).then(
                response => {
                    try{
                        if (response.success){
                            console.log('Room ' + room.roomNumber + ' has been added to clinic ' + clinic_id)
                            this.setState({name: '', address:'', rooms:'', alert: false, success: true})
                        }
                        else {
                            console.log('room addition not successful')
                        }
                    } catch(e){console.error("Error", e)}
                }
            ).catch((e)=>console.error("Error:", e))
        }
    }

    render() {
         let alert, success;

        if (this.state.alert){
            alert = <div className="flash animated" id="welcome"><Alert bsStyle="warning">Clinic already exists!</Alert></div>
        }
        else{
            alert = null
        }

        if (this.state.success){
            success = <div className="flash animated" id="welcome"><Alert bsStyle="success">Clinic registered!</Alert></div>
        }
        else{
            success = null
        }

        return (
            <div className="Register">
                {alert}
                {success}
                <form onSubmit={this.handleRegister}>
                    <FormGroup controlId="name" bsSize="large">
                        <ControlLabel>Clinic Name</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="ex: Concordia Urgent Care Clinic"
                        value={this.state.name}
                        onChange={this.handleChange}
                        />
                    </FormGroup>
                    <FormGroup controlId="address" bsSize="large">
                        <ControlLabel>Address</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="ex: Sir George Williams Campus. 1550 De Maisonneuve W. Room GM-200"
                        value={this.state.address}
                        onChange={this.handleChange}
                        />
                    </FormGroup>
                    <FormGroup controlId="rooms" bsSize="large">
                        <ControlLabel>Number of Rooms</ControlLabel>
                        <FormControl
                        type="text"
                        placeholder="ex: 5"
                        value={this.state.rooms}
                        onChange={this.handleChange}
                        />
                    </FormGroup>
                    <Button
                        block
                        bsSize="large"
                        type="submit"
                        disabled={!this.validateForm()}
                    >
                        Register
                    </Button>
                </form>
            </div>
        );
    }
}

export default RegisterClinic;