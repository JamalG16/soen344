import React, { Component } from 'react'
import { Row, Col, Grid } from 'react-bootstrap'
import Login from './Login'
import Register from './Register'
import CalendarPatient from './CalendarPatient'
import { connect } from 'react-redux'
import { Route } from 'react-router-dom'
import CalendarDoctor from "./CalendarDoctor";
import CalendarNurse from "./CalendarNurse";
import AppointmentCart from "./AppointmentCart";

class Body extends Component {

  constructor(props) {
    super(props);
    this.state = {
      
    };
  }
  render() {
    return (
      <div>
        <Grid>
          <Row>
              {/* body part */}
                <Route exact path='/' render={()=>{
                  return(
                    <div>
                      {Login}
                      {Register}
                      {CalendarPatient}
                      {CalendarDoctor}
                      {CalendarNurse}
                      {AppointmentCart}
                    </div>
                  )
                }} />
				<Route path='/Login' component={Login}/>
                <Route path='/Register' component={Register}/>
                <Route path='/CalendarPatient' component={CalendarPatient}/>
                <Route path='/CalendarDoctor' component={CalendarDoctor} />
                <Route path='/CalendarNurse' component={CalendarNurse} />
                <Route path='/AppointmentCart' component={AppointmentCart} />
          </Row>
        </Grid>
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    user: state.login.user
  }
}

Body = connect(
  mapStateToProps,
)(Body);

export default Body;
