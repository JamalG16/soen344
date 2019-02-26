import React, {Component} from 'react'
import {PageHeader, Button} from 'react-bootstrap'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'
import { Col, Row, Grid} from 'react-bootstrap'
import Menu from './Menu'

class Header extends Component {
  
  render() {
    return (
      <PageHeader>
        <Grid>
          <Row>
            <Col lg={2} lgOffset={0}>
              <h3>
                <Link to='/'>
                  Uber Santé 
                </Link>    
              </h3>
            </Col>
            <Col lg={3} lgOffset={7}>
              <h3>
                <Menu 
                user = {this.props.user}/>
              </h3>
            </Col>
          </Row>
        </Grid>
      </PageHeader>
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
