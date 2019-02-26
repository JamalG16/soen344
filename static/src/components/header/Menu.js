import React, {Component} from 'react'
import { Link } from 'react-router-dom'
import { logout } from '../../actions/auth'

class Menu extends Component {
    render() {
        let menu; 
        //TODO: IMPLEMENT CASE CHECKS TO DETERMINE IF LOGGED IN USER IS PATIENT/NURSE/DOCTOR/ADMIN AND DISPLAY
        //APPROPRIATE OPTIONS IN THE MENU
        if (this.props.user!=null) { 
            menu = <div>
                <Link to="/" onClick={logout}>
                    Logout
                </Link>
                <Link to="/book">
                    Book Appointment
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