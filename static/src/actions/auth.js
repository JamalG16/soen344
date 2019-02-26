import configureStore from '../store/configureStore'

export const login = (user) => {
    configureStore.store.dispatch({
        type:"USER_CONNECTION",
        payload: user
    })
    window.location.href = ((window.location.href).split('/login')[0])
}

export const logout = () => {
    configureStore.store.dispatch({
        type:"LOG_OUT"
    })
}

