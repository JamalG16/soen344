import React, { Component } from 'react'
import { Row, Col, Grid } from 'react-bootstrap'
import Login from './Login'
import { connect } from 'react-redux'
import { Route } from 'react-router-dom'

class Body extends Component {

  constructor(props) {
    super(props);
    this.state = {
      
    };
  }
  render() {
    let login;
    //if no user is logged in, then display login form, else, do not.
    if (1){
      
    } else {
      
    }

    return (
      <div>
        <Grid>
          <Row>
              {/* body part */}
                <Route exact path='/' render={()=>{
                  return(
                    <div>
                    {Login}
                  </div>
                  )
                }} />
				<Route path='/Login' component={Login}/>
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
