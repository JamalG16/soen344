import React, { Component } from "react";
import { connect } from 'react-redux'
import { FormGroup, FormControl, ControlLabel, Button, Alert } from "react-bootstrap";
import { fetchAPI } from '../utility'
import './update_availability.css'

class UpdateAvailability extends Component {
    constructor(props) {
        super(props)
     this.state = {
       month: -1,
       day: -1,
       buttons: [false, false, false, false, false, false,
                 false, false, false, false, false, false,
                 false, false, false, false, false, false,
                 false, false, false, false, false, false,
                 false, false, false, false, false, false,
                 false, false, false, false, false, false],
       update_success: ""
     }

     this.updateAvailability = this.updateAvailability.bind(this);
   }

   async updateAvailability(){
    var month = parseInt(this.state.month) + 1
    var date =  "-" + ((month < 10)? "0"+month : month) + "-" + ((this.state.day < 10)? "0"+this.state.day : this.state.day)
    var now = new Date()
    var year = now.getFullYear()
    if (now.getMonth() > this.state.month) {
        year++;
    }
    date = year + date
    let availability = {timeslots: this.state.buttons, date: date, permit_number: this.props.user.permit_number,
                        password_hash: this.props.user.password_hash}
    console.log(availability)
    fetchAPI("POST", "/api/doctor/availability/", availability).then(
      response => {
        try{
          this.setState({update_success: response.message}, () => { console.log(this.state.update_success)
                                                                    this.render()})
          if (response.success){
            console.log('it is a success mate')
          }
          else {
            console.log('it is a fail mate');
          }
        } catch(e){console.error("Error", e)}
      }
    ).catch((e)=>console.error("Error:", e))
  }

  getTable() {
    if (this.state.day == -1 || this.state.month == -1) {
        return
    }

    const list = this.state.buttons.map(item => { return (false)
                                         });
      this.setState({
            buttons: list
      }, () => {});

    var month = parseInt(this.state.month) + 1
    var date =  "-" + ((month < 10)? "0"+month : month) + "-" + ((this.state.day < 10)? "0"+this.state.day : this.state.day)
    var now = new Date()
    var year = now.getFullYear()
    if (now.getMonth() > this.state.month) {
        year++;
    }
    date = year + date

    fetchAPI("GET", "/api/doctor/availability?permit_number=" + this.props.user.permit_number +
                        "&password_hash=" + this.props.user.password_hash +
                        "&date=" + date).then(
      response => {
        try{
          if (response.success){
            console.log('it is a success mate')
            this.parseSchedule(response.schedule)
          }
          else {
            console.log('it is a fail mate');
          }
        } catch(e){console.error("Error", e)}
      }
    ).catch((e)=>console.error("Error:", e))
  }

    parseSchedule(schedule) {
      const list = schedule.map(item => {var string = JSON.stringify(item)
                                         var index = string.indexOf('t')
                                         if (index == -1) {
                                            index = string.indexOf('f')
                                         }
                                         return (string.substring(index, string.length-1) == 'true')
                                         });
      this.setState({
            buttons: list
      }, () => {});
    }

    getNbDayForMonth(month) {
        switch(month) {
            case "0":
            case "2":
            case "4":
            case "6":
            case "7":
            case "9":
            case "11":
                return 31
            case "3":
            case "5":
            case "8":
            case "10":
                return 30
            case "1":
                var now = new Date()
                var year = now.getFullYear()
                if (now.getMonth() > 1) {
                    year = year + 1
                }
                if (year % 400 == 0) {
                    return 29
                } else if (year % 100 == 0) {
                    return 28
                } else if (year % 4 == 0) {
                    return 29
                } else {
                    return 28
                }
            default:
                return 5
        }
    }


    getMonth(offset) {
        var monthStr = "";
        var month = new Date().getMonth() + offset;

        if (month > 11) {
            month = month - 12;
        }
        switch(month) {
            case 0:
                monthStr = "Jan";
                break;
            case 1:
                monthStr = "Feb";
                break;
            case 2:
                monthStr = "Mar";
                break;
            case 3:
                monthStr = "Apr";
                break;
            case 4:
                monthStr = "May";
                break;
            case 5:
                monthStr = "Jun";
                break;
            case 6:
                monthStr = "Jul";
                break;
            case 7:
                monthStr = "Aug";
                break;
            case 8:
                monthStr = "Sep";
                break;
            case 9:
                monthStr = "Oct";
                break;
            case 10:
                monthStr = "Nov";
                break;
            default:
                monthStr = "Dec";
                break;
        }
        return monthStr;
    }

    getMonths() {
        let months = []
        for (var i = 0; i <12; i++) {
            months.push(<option value={(new Date().getMonth() + i > 11) ? (new Date().getMonth() + i - 12) : new Date().getMonth() + i}>
                            {this.getMonth(i)}</option>)
        }
        let table = []
        table.push(<select id="month-select" onChange={(e) => { if (e.target.value != this.state.month)
                                                                    this.setState({
                                                                        month: e.target.value
                                                                        }, () => {this.getTable()})
                                                               }}
                    value={this.state.month}><option value="-1">Month</option>{months}</select>)
        return table
    }

    getDays() {
        let days = []
        var start = 1;
        var now = new Date();
        if (this.state.month == now.getMonth()) {
            start = now.getDate() + 1
        }
        for (var i = start; i <= this.getNbDayForMonth(this.state.month); i++) {
            days.push(<option value={i}>{i}</option>)
        }
        let table = []
        table.push(<select id="day-select" onChange={(e) => {  if (e.target.value != this.state.day) {
                                                                    this.setState({
                                                                        day: e.target.value
                                                                        }, () => {this.getTable()})
                                                               }}}
                    value={this.state.day}><option value="-1">Day</option>{days}</select>)
        return table
    }

    getTableRows() {
        let slots = []
        for (var i = 8; i < 20; i++) {
            for(var j = 0; j <3; j++) {
                var min = j*20
                if (min == 0) {
                    min = "00"
                }
                var offset = (i-8)*3 + j
                slots.push(<tr value={i + ":" + min}>
                                <td>{i + ":" + min}</td>
                                <td ><button className="available" onClick={(e) => {var index = e.target.name
                                                                                    let buttons = this.state.buttons
                                                                                    buttons[index] = !buttons[index]
                                                                                    this.setState({ buttons }, () => {});
                                                                                    }}
                                name={offset}>{(this.state.buttons[offset])? "Available" : "Unavailable"}</button></td>
                            </tr>
                            )
            }
        }

        let table = []
        table.push(<tbody>{slots}</tbody>)
        return table
    }

    render() {
        if (!(Object.keys(this.props.user).length === 0 && this.props.user.constructor === Object) && typeof(this.props.user.permit_number) !== 'undefined'){
            if (this.state.month == -1) {
            return (
                    <div>
                        {this.getMonths()}
                    </div>
            );
            } else if (this.state.day == -1) {
            return (
                    <div>
                        {this.getMonths()}
                        {this.getDays()}
                    </div>
            );
            } else {
            return (
                <div>
                    <div>
                        <div>
                            {this.getMonths()}
                            {this.getDays()}
                            <button onClick={this.updateAvailability}>update</button>
                        </div>
                        <div>
                            {this.state.update_success}
                        </div>
                        <div>
                            <table id="example" className="display">
                                <thead>
                                    <tr>
                                        <th>Time</th>
                                        <th>Available</th>
                                    </tr>
                                </thead>
                                {this.getTableRows()}
                            </table>
                        </div>
                    </div>
                </div>
                );
            }
        } else {
            return(<a href="/Homepage">Are you lost? go back to homepage</a>);
        }
    }
}

function mapStateToProps(state) {
  return {
    user: state.login.user
  }
}

UpdateAvailability = connect(
  mapStateToProps,
)(UpdateAvailability);

export default UpdateAvailability;