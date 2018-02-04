// Set up your application entry point here...
import React from 'react';
import ReactDOM from 'react-dom';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import MyAwesomeReactComponent from './components/MyAwesomeReactComponent';

const App = () => (
    <MuiThemeProvider>
        <MyAwesomeReactComponent />
    </MuiThemeProvider>
);

ReactDOM.render(
    <App />,
    document.getElementById('app')
);
