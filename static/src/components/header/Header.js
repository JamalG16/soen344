import React, {Component} from 'react'
import {PageHeader, Button} from 'react-bootstrap'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'
import { Col, Row, Grid} from 'react-bootstrap'
import Menu from './Menu'

class Header extends Component {
  
  render() {
    return (
        <Grid style={{background: '#F2F1F1', width: '100%'}}>
          <Row>
            <Col xs={6} style={{textAlign: 'left'}}>
              <h3>
                <Link to='/'>
                  Uber Santé 
                </Link>    
              </h3>
            </Col>
            <Col xs={6} style={{textAlign: 'right'}}>
              <h3>
                {<Menu 
                user = {this.props.user}/>}
              </h3>
            </Col>
          </Row>
        </Grid>
    );
  }
}

function mapStateToProps(state) {
  return {
    user: state.login.user
  }
}

Header = connect(
  mapStateToProps,
)(Header);

export default Header;
