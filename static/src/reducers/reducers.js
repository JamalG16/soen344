import { combineReducers } from 'redux'
import { reducer as formReducer } from 'redux-form';
/*
 CONNECTION REDUCER
 */
const INITIAL_STATE_LOGIN = { online: false, user: {},error:""};

const loginReducer = (state = INITIAL_STATE_LOGIN, action) => {
    switch (action.type) {
        case 'USER_CONNECTION': {
            return { ...state, user: action.payload.user, online: true,}
        }
        case 'ERROR_LOGIN': {
            return { ...state, error: action.payload }
        }
        case 'ERROR_CLEAR': {
            return { ...state, error: "" }
        }
        case 'IS_LOGGED': {
            return { ...state, logged: action.payload }
        }
        case 'LOG_OUT': {
            return { state: INITIAL_STATE_LOGIN }
        }
        default: {
            return state
        }

    }
};



const rootReducer = combineReducers({
    form: formReducer,
    login: loginReducer
});
export default rootReducer
