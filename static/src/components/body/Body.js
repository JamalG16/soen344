import React, { Component } from 'react'
import { Row, Col, Grid } from 'react-bootstrap'
import Login from './login//Login'
import Register from './register/Register'
import CalendarPatient from './calendars/CalendarPatient'
import { connect } from 'react-redux'
import { Route } from 'react-router-dom'
import CalendarDoctor from "./calendars/CalendarDoctor";
import CalendarNurse from "./calendars/CalendarNurse";
import AppointmentCart from "./AppointmentCart";
import Homepage from "./homepages/Homepage";
import UpdateAvailability from "./doctor avail/UpdateAvailability"

class Body extends Component {

  constructor(props) {
    super(props);
    this.state = {
      cart: []
    };
    this.addToCart = this.addToCart.bind(this);
    this.removeFromCart = this.removeFromCart.bind(this);
  }

  addToCart(appointment){
    var exists = false
    this.state.cart.map(function(cartObject){
      if(appointment[0] == cartObject[0] && appointment[1] == cartObject[1] && appointment[2] == cartObject[2])
        exists = true
    })
    if (!exists)
      this.setState({cart: this.state.cart.concat([appointment])});
  }

  removeFromCart(appointment){
    var cartCopy = [...this.state.cart];
    var index = cartCopy.indexOf(appointment)
    if (index !== -1){
      cartCopy.splice(index,1);
      this.setState({cart: cartCopy})
    }
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
                      {UpdateAvailability}
                      {CalendarPatient}
                      {CalendarDoctor}
                      {CalendarNurse}
                      {AppointmentCart}
                      {Homepage}
                    </div>
                  )
                }} />
				        <Route path='/Login' component={Login}/>
                <Route path='/Register' component={Register}/>
                <Route path='/UpdateAvailability' component={UpdateAvailability}/>
                <Route path='/CalendarPatient' render={(props) => <CalendarPatient {...props} addToCart={this.addToCart} cart={this.state.cart}/>}/>
                <Route path='/CalendarDoctor' component={CalendarDoctor} />
                <Route path='/CalendarNurse' component={CalendarNurse} />
                <Route path='/AppointmentCart' render={(props) => <AppointmentCart {...props} removeFromCart={this.removeFromCart} cart={this.state.cart} user={this.props.user}/>}/>
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
