import * as actionTypes from '../constants/actionTypes';

const DEFAULT_STATE = {
    ajaxCallsInprogress: 0,
};

function actionTypeEndsInSuccess(type) {
    return type.endsWith('_SUCCESS');
}

export default function ajaxReducer(state = DEFAULT_STATE, action) {
    if (action.type == actionTypes.BEGIN_AJAX_CALL)
        return {
            ...state,
            ajaxCallsInprogress: state.ajaxCallsInprogress + 1,
        };
    else if (state > 0 && (actionTypes.AJAX_CALL_ERROR || actionTypeEndsInSuccess(action.type)))
        return {
            ...state,
            ajaxCallsInprogress: state.ajaxCallsInprogress - 1,
        };
    return state;
}
