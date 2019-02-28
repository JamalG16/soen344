
import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import configureStore from './store/configureStore'
import App from './containers/App'
import { PersistGate } from 'redux-persist/integration/react'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';

const target = document.querySelector('#root');

ReactDOM.render(
    <Provider store={configureStore.store}>
        <PersistGate loading={null} persistor={configureStore.persistor}>
            <App />
        </PersistGate>
    </Provider>,
    target
);