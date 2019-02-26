import React, {Component} from 'react'
import { Link } from 'react-router-dom'
import { logout } from '../../actions/auth'

class Menu extends Component {
    render() {
        let menu; 
        if (this.props.user!==null && this.props.user!==hcnumber) { //if patient is logged in, display logout
            menu = <div>
                <Link to="/" onClick={logout}>
                    Logout
                </Link>
                <Link to="/book">
                    Book Appointment
                </Link>
            </div>
        //add cases for nurse, doctors and admins
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