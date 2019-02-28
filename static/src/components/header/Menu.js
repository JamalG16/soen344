import React, {Component} from 'react'
import { Link } from 'react-router-dom'
import PatientMenu from './PatientMenu'
import AdminMenu from './AdminMenu'
import NurseMenu from './NurseMenu'
import DoctorMenu from './DoctorMenu'

class Menu extends Component {
    render() {
        let menu; 
        //if patient is logged in
        if (!(Object.keys(this.props.user).length === 0 && this.props.user.constructor === Object) && typeof(this.props.user.hcnumber) !== 'undefined') { 
            menu = <div>
                <PatientMenu user={this.props.user}/>
            </div>
        //if doc is logged in
        } else if (!(Object.keys(this.props.user).length === 0 && this.props.user.constructor === Object) && typeof(this.props.user.permit_number) !== 'undefined') { 
            menu = <div>
                <DoctorMenu user={this.props.user}/>
            </div>
        //if nurse is logged in
        } else if (!(Object.keys(this.props.user).length === 0 && this.props.user.constructor === Object) && typeof(this.props.user.access_ID) !== 'undefined') { 
            menu = <div>
                <NurseMenu user={this.props.user}/>
            </div>
        //if admin is logged in
        } else if (!(Object.keys(this.props.user).length === 0 && this.props.user.constructor === Object) && typeof(this.props.user.username) !== 'undefined') { 
            menu = <div>
                <AdminMenu user={this.props.user}/>
            </div> 
        //no user is connected, display login and register    
        } else { 
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