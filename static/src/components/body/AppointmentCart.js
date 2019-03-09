import {Component} from "react";
import React from "react";
import {Table, Button, Checkbox, Modal, Input} from 'antd';
import * as moment from 'moment';
import 'antd/es/table/style/index.css';
import 'antd/es/modal/style/index.css';


class AppointmentCart extends Component {

    state = { visible: false }

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

    render() {
        return (
            <div>
                <h1>Appointment Cart</h1>
                <TableGenerator />
                <Button style={{float:'right', color:'red'}} onClick={this.showModal} size="large">Remove</Button>
                <Button style={{float:'right', color:'blue'}} onClick={this.showModal} size="large">Check-Out</Button>
                <Modal
                    title="Credit Card Information"
                    visible={this.state.visible}
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                    okButtonProps={{ disabled: true }}
                    cancelButtonProps={{ disabled: true }}
                >
                    Name on card
                    <Input placeholder="" />
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

function TableGenerator(props) {


    let success = props.success;
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
            title: <div style={{float:'right'}}>Select</div>,
        dataIndex: 'select'
    }
    ];

    const data = [{
        type: 'Annual',
        time: moment().format('HH:MM'),
        date: '5th',
        price: '50$',
        select: <Checkbox style={{float:'right'}} onChange={onChange}></Checkbox>
    },
    {
        type: 'Check-In',
        time: moment().format('HH:MM'),
        date: '5th',
        price: '50$',
        select: <Checkbox style={{float:'right'}} onChange={onChange}></Checkbox>
    }
    ];

    return (
        <div>
            <Table columns={columns} dataSource={data} pagination={false}/>
        </div>
    );
}



function onChange(e) {
    console.log(`checked = ${e.target.checked}`);
}

export default AppointmentCart;