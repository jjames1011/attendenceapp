import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import * as actions from '../actions/loginActions';
import LoginDialog from '../components/LoginDialog';

class LoginPage extends React.Component {
    state = {
        username: '',
        password: '',
        isLoggingIn: false,
        isLoginFailed: false,
    };

    handleUsernameChange = (event) => {
        this.setState({
            username: event.target.value,
        });
    };

    handlePasswordChange = (event) => {
        this.setState({
            password: event.target.value,
        });
    };

    handleLogin = () => {
        this.setState({
            isLoggingIn: true,
            isLoginFailed: false,
        });

        this.props.actions.login(
            this.state.username,
            this.state.password);

        setTimeout(() => {
            this.setState({
                isLoggingIn: false,
                isLoginFailed: true,
            });
        }, 2000);
    };

    render() {
        return (
            <LoginDialog
                username={this.state.username}
                password={this.state.password}
                onUsernameChange={this.handleUsernameChange}
                onPasswordChange={this.handlePasswordChange}
                onLogin={this.handleLogin}
                isLoggingIn={this.state.isLoggingIn}
                isLoginFailed={this.state.isLoginFailed}
                shouldDisplayForgotPassword={this.state.shouldDisplayForgotPassword}/>
        );
    }
}

LoginPage.propTypes = {
    actions: PropTypes.object.isRequired,
};

function mapStateToProps(state) {
    return {

    };
}

function mapDispatchToProps(dispatch) {
    return {
        actions: bindActionCreators(actions, dispatch)
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(LoginPage);
