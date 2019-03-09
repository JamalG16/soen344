import {Component} from "react";
import React from "react";
import {Card} from 'antd';
import 'antd/es/card/style/index.css';

class HomepagePatient extends Component {
 constructor(props) {
        super(props)
    }

    render(){
     //Temporary mock appointments for user
    const appointments = [
        {
            date: 'April 4th 2019',
            doctor: 'Dr Slanjki Pans',
            type: 'annual'
        },

        {
            date: 'October 7 2020',
            doctor: 'Dr Svet Ampeet',
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
                     <p>{appointment.type} appointment with {appointment.doctor}</p>
                </Card>
                <br/>
            </div>
         )
     });

       return (
           <div>
               <br/>
               <h3>Upcoming appointments:</h3>
               {cardList}
           </div>
       );
    }
}

export default HomepagePatient;