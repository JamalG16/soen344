import {Component} from "react";
import React from "react";
import {Table, Button, Checkbox, Modal, Input, Popconfirm, message} from 'antd';
import * as moment from 'moment';
import 'antd/es/table/style/index.css';
import 'antd/es/modal/style/index.css';
import 'antd/es/message/style/index.css';
import 'antd/es/popconfirm/style/css.js';


class AppointmentCart extends Component {
    constructor() {
        super();
        this.state = { visible: false , selected: []}
    }

    showModal = () => {
        this.setState({
            visible: true,
        });
    }

    handleOk = (e) => {
        console.log(e);
        this.setState({
            visible: false,
        });
    }

    handleCancel = (e) => {
        console.log(e);
        this.setState({
            visible: false,
        });
    }

    TableGenerator() {

        const columns = [
            {
                title: 'Type',
                dataIndex: 'type',
            }, {
                title: 'Time',
                dataIndex: "time"
            }, {
                title: 'Date',
                dataIndex: 'date',
            }, {
                title: 'Price',
                dataIndex: 'price',
            }, {
                title: <div style={{float: 'right'}}>Select</div>,
                dataIndex: 'select'
            }
        ];

        const data = []
        this.props.cart.map(function(appointment){
            data.push({
                type: appointment[0],
                time: appointment[2],
                date: appointment[1],
                price: '50$',
                select: <Checkbox style={{float: 'right'}} onChange={onChange}></Checkbox>
            })
        })

        return (
            <div>
                <Table columns={columns} dataSource={data} pagination={false}/>
            </div>
        );
    }

    /*async checkout(){
        let data = {hcnumber: this.props.user.hcnumber, length:, time: , date: }
        fetchAPI("POST", "/api/appointment/book", data).then(
            response => {
              try{
                if (response.success){
                    console.log('it is a success mate')
                }
                else {
                  console.log('it is a fail mate' + response.message);
                }
              } catch(e){console.error("Error", e)}
            }
          ).catch((e)=>console.error("Error:", e))
    }*/

    render() {

        return (
            <div>
                <h1>Appointment Cart</h1>
                {this.TableGenerator()}
                <Popconfirm title="Are you sure you want to remove these?" onConfirm={confirmation}  okText="Yes" cancelText="No">
                    <Button style={{float:'right', color:'red'}} size="large">Remove</Button>
                </Popconfirm>
                <Button style={{float:'right', color:'blue'}} onClick={this.showModal} size="large">Check-Out</Button>
                <Modal
                    title="Credit Card Information"
                    visible={this.state.visible}
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                >
                    Name on card
                    <Input name placeholder="" />
                    <br />
                    Card number
                    <Input placeholder="" />
                    <br />
                    Expiry Date
                    <Input placeholder="" />
                    <br />
                    Security code
                    <Input placeholder="" />
                    <br />
                    Zip/Postal code
                    <Input placeholder="" />
                </Modal>
            </div>
        );
    }
}

function onChange(e) {
    if (e.target.checked)
        this.setState({selected : this.state.selected.append([[e.target.type], [e.target.time], [e.target.date]])})
    console.log(this.state.selected);
}

function confirmation() {
    message.info('Removed');
}

export default AppointmentCart;