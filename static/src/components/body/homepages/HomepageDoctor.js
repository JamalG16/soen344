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
            clinics: []
        };
        this.getClinics()
        this.generateCardList = this.generateCardList.bind(this)
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
                    }
                    else {
                        console.log("Doctor " + this.props.user.permit_number + " failed to retrieve appointments")
                    }
                    this.generateCardList();
                } catch(e) {console.error("Error getting appointments for Doctor:", e)}
            }
        ).catch((e)=>console.error("Error getting appointments for Doctor:", e))
    }

    async generateCardList() {
        let appointmentsAsCards = this.state.clinics.map((clinic) => {
           return (
               appointmentsAsCards = this.state.appointments.map((appointment) => {
                   if (appointment.clinic_id == clinic.id){
                       return (
                           <div>
                               <Card
                                   title={appointment.date}
                                   style={{ width: 800 }}>
                                   <p>{appointment.length} minute appointment with patient: {appointment.patient_hcnumber}</p>
                                   <p>Clinic: {clinic.name}</p> 
                                   <p>Address: {clinic.address}</p>
                                   <p>Room: {appointment.room}</p>
                                   <p>Time: {appointment.time}</p>
                               </Card>
                               <br/>
                           </div>
                       )
                   }
                   else
                       return
                   })
               )
           });
        this.setState({cardList: appointmentsAsCards, isLoading: false})
    }

    async getClinics(){
        fetchAPI("GET", '/api/clinic/findAll').then(
            response => {
                try{
                    if(response.success){
                        this.setState({
                            clinics: response.clinics
                        });
                        console.log('retrieved clinics')
                    }
                    else {
                        console.log('failed to retrieve clinics')
                    }
                    this.handleAppointmentsDoctor();
                } catch(e) {console.error("Error getting appointments for patient:", e)}
            }
        ).catch((e)=>console.error("Error getting appointments for patient:", e))
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