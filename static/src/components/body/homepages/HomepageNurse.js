import {Component} from "react";
import React from "react";
import {Tab, Tabs} from "react-bootstrap";
import RegisterPatient from "../Register";
import CalendarPatient from "../CalendarPatient";
import HomepagePatient from "./HomepagePatient";
import CalendarDoctor from "../CalendarDoctor";
import HomepageDoctor from "./HomepageDoctor";

class HomepageNurse extends Component {
    render(){
       return (
           <div>
               <h2>Choose Patient or Doctor to Book, Edit, or Cancel an appointment</h2>
                <Tabs defaultActiveKey="patient" id="uncontrolled-tab-example">
                    <Tab eventKey="patient" title="Patient">
                        <Tabs defaultActiveLey="book">
                            <Tab eventKey="book" title="Book">
                                &nbsp;
                                <CalendarPatient/>
                            </Tab>
                            <Tab eventKey="edit" title="Edit">
                                <HomepagePatient/>
                            </Tab>
                            <Tab eventKey="cancel" title="Cancel">
                                <HomepagePatient/>
                            </Tab>
                        </Tabs>
                    </Tab>
                    <Tab eventKey="doctor" title="Doctor">
                        <Tabs defaultActiveLey="book">
                            <Tab eventKey="book" title="Book">
                                &nbsp;
                                <CalendarDoctor/>
                            </Tab>
                            <Tab eventKey="edit" title="Edit">
                                <HomepageDoctor/>
                            </Tab>
                            <Tab eventKey="cancel" title="Cancel">
                                <HomepageDoctor/>
                            </Tab>
                        </Tabs>
                    </Tab>
                </Tabs>
            </div>
       );
    }
}

export default HomepageNurse;