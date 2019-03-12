import {Component} from "react";
import React from "react";
import {Table, Button, Checkbox, Modal, Input, Popconfirm, message} from 'antd';
import { fetchAPI } from '../utility'
import 'antd/es/table/style/index.css';
import 'antd/es/modal/style/index.css';
import 'antd/es/message/style/index.css';
import 'antd/es/popconfirm/style/css.js';


class AppointmentCart extends Component {
    constructor(props) {
        super(props);
        this.state = { visible: false, length: '', date:'', time:'' }
        this.onCheckout = this.onCheckout.bind(this)
        this.TableGenerator = this.TableGenerator.bind(this)
    }

    showModal = () => {
        this.setState({
            visible: true,
        });
    }

    handleOk = (e) => {
        this.setState({
            visible: false,
        });
        this.checkout()
    }

    handleCancel = (e) => {
        this.setState({
            visible: false,
            length: '',
            date: '',
            time: '',
        });
    }

    onCheckout(appointment){
        if (appointment[0] == 'Checkup'){
            this.setState({length:'20', date: appointment[1], time: appointment[2]})
            this.showModal()
        }
        if (appointment[0] == 'Annual'){
            this.setState({length:'60', date: appointment[1], time: appointment[2]})
            this.showModal()
        }
    }
    
    onRemove(appointment){
        this.setState({
            length: '',
            date: '',
            time: '',
        });
        this.props.removeFromCart(appointment)
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
                title: <div style={{float: 'left'}}>Action</div>,
                dataIndex: 'button'
            }
        ];

        const data = []
        this.props.cart.map((appointment) => {
            data.push({
                type: appointment[0],
                time: appointment[2],
                date: appointment[1],
                price: '50$',
                button: <div>
                    <Button type="primary" icon="minus" style={{float: 'left'}} size="large" onClick={() => 
                    this.onRemove(appointment)}>Remove</Button>
                    <Button type="primary" icon="plus" style={{float: 'right'}} size="large" onClick={() => 
                    this.onCheckout(appointment)}>Checkout</Button>
                    </div>
            })
        })

        return (
            <div>
                <Table columns={columns} dataSource={data} pagination={false}/>
            </div>
        );
    }

    async checkout(){
        let appointment = {hcnumber: this.props.user.hcnumber, length: this.state.length, time:this.state.time , date:this.state.date }
        fetchAPI("PUT", "/api/appointment/book", appointment).then(
            response => {
              try{
                if (response.success){
                    console.log('it is a success mate')
                    if (this.state.length=='20')
                     this.onRemove(['Checkup', this.state.date, this.state.time])
                    else
                     this.onRemove(['Annual', this.state.date, this.state.time])
                }
                else {
                  console.log('it is a fail mate' + response.message + response.info);
                }
              } catch(e){console.error("Error", e)}
            }
          ).catch((e)=>console.error("Error:", e))
    }

    render() {

        return (
            <div>
                <h1>Appointment Cart</h1>
                {this.TableGenerator()}
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

function confirmation() {
    message.info('Removed');
}

export default AppointmentCart;