
import React, { Component } from 'react';
import Body from '../components/body/Body';
import Header from '../components/header/Header';
import Infodump from './Infodump';
import { BrowserRouter as Router, Route } from 'react-router-dom';

export class App extends Component {



  render() {
    
    return (
      <div >
        <Router>
          <div>
          <Header />
          <Route path='/' component={Body}/>
          <Infodump></Infodump>
          </div>
        </Router>
      </div>
    )
  }

}
export default App;
