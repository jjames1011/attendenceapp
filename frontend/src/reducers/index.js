import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';
import ajaxReducer from './ajaxReducer';
import loginReducer from './loginReducer';

const rootReducer = combineReducers({
    ajaxReducer,
    loginReducer,
    routerReducer,
});

export default rootReducer;
