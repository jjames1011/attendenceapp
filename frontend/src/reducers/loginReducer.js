import * as actionTypes from '../constants/actionTypes';

const DEFAULT_STATE = {
    username: '',
    password: '',
    isLoading: false,
    hasError: false,
};

export default function loginReducer(state = DEFAULT_STATE, action) {
    switch (action.type) {
        case actionTypes.LOGIN:
            return {
                ...state,
                isLoading: true,
                hasError: false,
            };
        case actionTypes.LOGIN_SUCCESS:
            return {
                ...state,
                isLoading: false,
                hasError: false,
            };
        case actionTypes.LOGIN_FAIL:
            return {
                ...state,
                isLoading: false,
                hasError: true,
            };
        default:
            return state;
    }
}
