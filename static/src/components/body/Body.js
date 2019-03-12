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
import Homepage from "./homepages/Homepage";

class Body extends Component {

  constructor(props) {
    super(props);
    this.state = {
      cart: [['Checkup','2019-04-05','8:00'],['Checkup','2019-04-05','8:20']]
    };
  }

  addToCart(appointment){
    this.setState({cart: this.state.cart.concat([appointment])});
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
                      {<CalendarPatient addToCart={this.addToCart.bind(this)} cart={this.state.cart}/>}
                      {CalendarDoctor}
                      {CalendarNurse}
                      {<AppointmentCart cart={this.state.cart}/>}
                      {Homepage}
                    </div>
                  )
                }} />
				        <Route path='/Login' component={Login}/>
                <Route path='/Register' component={Register}/>
                <Route path='/CalendarPatient' component={CalendarPatient} addToCart={this.addToCart.bind(this)} cart={this.state.cart}/>
                <Route path='/CalendarDoctor' component={CalendarDoctor} />
                <Route path='/CalendarNurse' component={CalendarNurse} />
                <Route path='/AppointmentCart' component={AppointmentCart} cart={this.state.cart}/>
                <Route path='/Homepage' component={Homepage} />
          </Row>
        </Grid>
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    user: state.login.user,
  }
}

Body = connect(
  mapStateToProps,
)(Body);

export default Body;
