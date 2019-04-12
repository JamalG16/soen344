import React, {Component} from 'react'
import { Link } from 'react-router-dom'
import { logOut } from '../../actions/auth'


class AdminMenu extends Component {
    render() {
        return (
            <div>
                    Welcome {this.props.user.username}!
                    &nbsp;&nbsp;&nbsp;
                    <Link to="/Register">
                        Registration
                    </Link>
                    &nbsp;&nbsp;&nbsp;
                    <Link to="/Clinics">
                    Clinics
                    </Link>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <Link to="/Homepage" onClick={logOut}>
                        Logout
                    </Link>
            </div> 
        );
    }
}


export default AdminMenu;