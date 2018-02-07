import * as actionTypes from '../constants/actionTypes';

export function beginAjaxCall() {
    return {
        type: actionTypes.BEGIN_AJAX_CALL,
    };
}

export function ajaxCallError() {
    return {
        type: actionTypes.AJAX_CALL_ERROR,
    };
}
