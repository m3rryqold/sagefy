const {dispatch} = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')

module.exports = tasks.add({
    createUser(data) {
        dispatch({
            type: 'SET_SENDING_ON'
        })
        dispatch({type: 'CREATE_USER'})
        return request({
            method: 'POST',
            url: '/s/users',
            data: data,
        })
            .then((response) => {
                dispatch({
                    type: 'SET_CURRENT_USER_ID',
                    currentUserID: response.user.id,
                    message: 'create user success',
                })
                // TODO-2 make this a listener
                window.location = '/my_sets'
                // Hard redirect to get the HTTP_ONLY cookie
                // TODO-1 if set_id is a param, auto add to user's sets
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'create user failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    updateUser(data) {
        dispatch({
            type: 'SET_SENDING_ON'
        })
        dispatch({type: 'UPDATE_USER', id: data.id})
        return request({
            method: 'PUT',
            url: `/s/users/${data.id}`,
            data: data,
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_USER',
                    user: response.user,
                    message: 'update user success',
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'update user failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    getCurrentUser() {
        dispatch({type: 'GET_CURRENT_USER'})
        return request({
            method: 'GET',
            url: '/s/users/current',
        })
            .then((response) => {
                dispatch({
                    type: 'SET_CURRENT_USER_ID',
                    currentUserID: response.user.id,
                })
                dispatch({
                    type: 'ADD_USER',
                    user: response.user,
                    message: 'get current user success',
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'get current user failure',
                    errors,
                })
            })
    },

    getUser(id, opts = {}) {
        dispatch({type: 'GET_USER', id})
        return request({
            method: 'GET',
            url: `/s/users/${id}`,
            data: opts,
        })
            .then((response) => {
                const user = response.user
                ;['avatar', 'posts', 'sets', 'follows'].forEach((t) => {
                    if (response[t]) { user[t] = response[t] }
                })
                dispatch({
                    type: 'ADD_USER',
                    message: 'get user success',
                    user,
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'get user failure',
                    errors,
                })
            })
    },

    logInUser(data) {
        dispatch({
            type: 'SET_SENDING_ON'
        })
        dispatch({type: 'LOG_IN_USER'})
        return request({
            method: 'POST',
            url: '/s/sessions',
            data: data,
        })
            .then((response) => {
                dispatch({
                    type: 'SET_CURRENT_USER_ID',
                    currentUserID: response.user.id,
                    message: 'log in user success',
                })
                // Hard redirect to get the HTTP_ONLY cookie
                // TODO-2 move to listener
                window.location = '/my_sets'
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'log in user failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    logOutUser() {
        dispatch({
            type: 'SET_SENDING_ON'
        })
        dispatch({type: 'LOG_OUT_USER'})
        return request({
            method: 'DELETE',
            url: '/s/sessions',
        })
            .then(() => {
                dispatch({
                    type: 'RESET_CURRENT_USER_ID',
                    messsage: 'log out user success',
                })
                window.location = '/'
                // Hard redirect to delete the HTTP_ONLY cookie
                // TODO-2 move to listener
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'log out user failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    getUserPasswordToken(data) {
        dispatch({
            type: 'SET_SENDING_ON'
        })
        dispatch({type: 'GET_PASSWORD_TOKEN'})
        return request({
            method: 'POST',
            url: '/s/password_tokens',
            data: data,
        })
            .then(() => {
                dispatch({
                    type: 'SET_PASSWORD_PAGE_STATE',
                    state: 'inbox',
                    message: 'get password token success',
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'get password token failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    createUserPassword(data) {
        dispatch({
            type: 'SET_SENDING_ON'
        })
        dispatch({type: 'CREATE_PASSWORD'})
        return request({
            method: 'POST',
            url: `/s/users/${data.id}/password`,
            data: data,
        })
            .then((response) => {
                dispatch({
                    type: 'SET_CURRENT_USER_ID',
                    message: 'create password success',
                    currentUserID: response.user.id,
                })
                // Hard redirect to get the HTTP_ONLY cookie
                // TODO-2 move to listener
                window.location = '/my_sets'
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'create password failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    }
})
