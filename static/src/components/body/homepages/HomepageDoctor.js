import {Component} from "react";
import React from "react";
import {Card, Modal, Button} from 'antd';
import 'antd/es/card/style/index.css';
import 'antd/es/modal/style/index.css';
import {fetchAPI} from "../../utility";

class HomepageDoctor extends Component {
 constructor(props) {
        super(props);
        this.state = {
            appointments:[],
            cardList:'',
            isLoading: true,
        };
        this.handleAppointmentsDoctor();
        this.generateCardList = this.generateCardList.bind(this)
    }

    // Functional but state not properly updating
    async getClinicForEachAppointment(){
        var modifiedAppts = [...this.state.appointments];
        modifiedAppts.forEach(function(appointment) {
            fetchAPI("POST", "/api/clinic/find", {clinic_id: appointment.clinic_id}).then(
                response => {
                    try{
                        if(response.success){
                            console.log('success') 
                            appointment.clinicInfo = response.clinic.name + ", " + response.clinic.address
                        }
                        else {
                            console.log('big fail')
                        }
                    } catch(e){console.error("Error", e)}
                }
            ).catch((e)=>console.error("Error:", e))
        })
        this.setState({appointments: modifiedAppts}, () => {})
        this.generateCardList();
    }

    async handleAppointmentsDoctor(){
        let route = "/api/appointment/checkDoctor?doctor_permit_number=" + this.props.user.permit_number;
        console.log(route);
        fetchAPI("GET",route).then(
            response => {
                try{
                    if(response.success){
                        this.setState({
                            appointments: response.appointments
                        });
                        console.log("Doctor " + this.props.user.permit_number + " successfully retrieved appointments")
                        this.getClinicForEachAppointment();
                    }
                    else {
                        console.log("Doctor " + this.props.user.permit_number + " failed to retrieve appointments")
                    }
                } catch(e) {console.error("Error getting appointments for Doctor:", e)}
            }
        ).catch((e)=>console.error("Error getting appointments for Doctor:", e))
    }

    async generateCardList() {
        let appointmentsAsCards = this.state.appointments.map(function (appointment) {
            console.log(appointment)
            console.log(Object.keys(appointment))
            return (
                <div>
                    <Card
                    title={appointment.date}
                    style={{ width: 800 }}>
                        <p>{appointment.length} minute appointment with patient: {appointment.patient_hcnumber}</p>
                        <p>Clinic id: {appointment.clinic_id}</p>
                        <p>Room: {appointment.room}</p>
                        <p>Time: {appointment.time}</p>
                </Card>
                <br/>
            </div>
            )
        });
        this.setState({cardList: appointmentsAsCards, isLoading: false})
    }

    render(){
       return (
           <div>
               <br/>
               <br/>
               <br/>
               <h3>Upcoming appointments:</h3>
               {this.state.isLoading ? 'Loading...' : this.state.cardList}
           </div>
       );
    }
}
export default HomepageDoctor;