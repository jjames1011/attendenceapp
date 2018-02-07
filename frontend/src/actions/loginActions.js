import * as actionTypes from '../constants/actionTypes';

export function login(username, password) {
    return function(dispatch) {
        console.log('Login: ' + username + ' ' + password);
        return dispatch({
            type: actionTypes.LOGIN,
        });
    };
}
