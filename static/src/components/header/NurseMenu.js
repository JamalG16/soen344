import React, {Component} from 'react'
import { Link } from 'react-router-dom'
import { logOut } from '../../actions/auth'

class PatientMenu extends Component {
  
  render() {
    return (
        <div>
            Welcome {this.props.user.fname}!
            &nbsp;&nbsp;&nbsp;&nbsp;
            <Link to="/Clinics">
              Clinics
            </Link>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <Link to="/Homepage" onClick={logOut}>
                Logout
            </Link>
        </div>
    );
  }
}


export default PatientMenu;
