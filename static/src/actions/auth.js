import configureStore from '../store/configureStore'

export const login = (user) => {
    configureStore.store.dispatch({
        type:"USER_CONNECTION",
        payload: user
    })
    window.location.href = "/Homepage"
}

export const logOut = () => {
    configureStore.store.dispatch({
        type:"LOG_OUT"
    })
}

