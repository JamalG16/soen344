import {Component} from "react";
import React from "react";
import {Card, Modal, Button} from 'antd';
import 'antd/es/card/style/index.css';
import 'antd/es/modal/style/index.css';

class HomepageDoctor extends Component {
 constructor(props) {
        super(props)
    }

    render(){
     //Temporary mock appointments for user
    const appointments = [
        {
            date: 'April 4th 2019',
            timeslot: '8:00-9:00',
            patient: 'Mr Ponny Panffs',
            type: 'annual'
        },

        {
            date: 'October 7 2020',
            timeslot: '16:20 - 16:40',
            patient: 'Ms Dar Knessi',
            type: 'check-in'
        }
    ];
     var cardList = appointments.map(function (appointment) {
         return (
             <div>
                 <Card
                    title={appointment.date}
                    extra={<a href="#">edit</a>}
                    style={{ width: 800 }}>
                     <p>{appointment.type} appointment with {appointment.patient}</p>
                     <p>Time: {appointment.timeslot}</p>
                </Card>
                <br/>
            </div>
         )
     });

       return (
           <div>
               <br/>
               <br/>
               <br/>
               <h3>Upcoming appointments:</h3>
               {cardList}
           </div>
       );
    }
}
export default HomepageDoctor;