import React, {Component} from 'react'
import { Link } from 'react-router-dom'
import { logOut } from '../../actions/auth'
import { Col } from 'react-bootstrap'

class Menu extends Component {
    render() {
        let menu; 
        //TODO: IMPLEMENT CASE CHECKS TO DETERMINE IF LOGGED IN USER IS PATIENT/NURSE/DOCTOR/ADMIN AND DISPLAY
        //APPROPRIATE OPTIONS IN THE MENU
        if (!(Object.keys(this.props.user).length === 0 && this.props.user.constructor === Object) && typeof(this.props.user.hcnumber) !== 'undefined') { 
            menu = <div>
                Welcome {this.props.user.fname}!
                &nbsp;&nbsp;&nbsp;&nbsp;
                <Link to="/book">
                    Book an Appointment
                </Link>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <Link to="/" onClick={logOut}>
                    Logout
                </Link>
            </div>
        } else if (!(Object.keys(this.props.user).length === 0 && this.props.user.constructor === Object) && typeof(this.props.user.username) !== 'undefined') { 
            menu = <div>
                Welcome {this.props.user.username}!
                &nbsp;&nbsp;&nbsp;&nbsp;
                <Link to="/register">
                    Register An Account
                </Link>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <Link to="/" onClick={logOut}>
                    Logout
                </Link>
            </div> 
        } else { //no user is connected, display login and register
            menu = <div>
                <Link to="/register">
                    Register
                </Link>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <Link to="/login">
                    Login
                </Link>
            </div>
        }
        return (
            <div>
            {menu}
            </div>
        );
    }
}

export default Menu;