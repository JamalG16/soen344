import {Component} from "react";
import React from "react";
import {Card} from 'antd';
import 'antd/es/card/style/index.css';
import 'antd/es/modal/style/index.css';
import {fetchAPI} from "../utility"

class Clinics extends Component {
 constructor(props) {
        super(props);
        this.state = {
            appointments:[],
            cardList:'',
            isLoading: true,
            clinics: []
        };
        this.getClinics();
    }

    async getClinics(){
        fetchAPI("GET", '/api/clinic/findAll').then(
            response => {
                try{
                    if(response.success){
                        this.setState({
                            clinics: response.clinics
                        });
                        console.log('retrieved clinics')
                    }
                    else {
                        console.log('failed to retrieve clinics')
                    }
                    this.generateCardList();
                } catch(e) {console.error("Error getting appointments for patient:", e)}
            }
        ).catch((e)=>console.error("Error getting appointments for patient:", e))
    }

    async generateCardList() {
        let clinicsAsCards = this.state.clinics.map((clinic) => {
            return (
                <div>
                    <Card
                        title={"Clinic ID: " + clinic.id}
                        style={{ width: 800 }}>
                        <p>Name: {clinic.name}</p> 
                        <p>Address: {clinic.address}</p>
                    </Card>
                    <br/>
                </div>
            )
        });
        this.setState({cardList: clinicsAsCards, isLoading: false})
    }

    render(){
       return (
            <div>
                <br/>
                <br/>
                <br/>
                <h3>Clinics:</h3>
                {this.state.isLoading ? 'Loading...' : this.state.cardList}
            </div>
       );
    }
}
export default Clinics;