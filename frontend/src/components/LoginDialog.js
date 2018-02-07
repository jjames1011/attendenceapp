import React from 'react';
import PropTypes from 'prop-types';
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import { CircularProgress } from 'material-ui/Progress';
import Dialog, {
    DialogActions,
    DialogContent,
    DialogTitle,
} from 'material-ui/Dialog';
import './LoginDialog.css';

const LoginDialog = ({
    username,
    password,
    onUsernameChange,
    onPasswordChange,
    onLogin,
    isLoggingIn,
    isLoginFailed,
}) => {
    const handleKey = event => {
        if (event.key === 'Enter' && username && password) {
            onLogin();
        }
    };

    return (
        <Dialog
            open={true}
            aria-labelledby="form-dialog-title">

            <DialogTitle id="form-dialog-title">Login</DialogTitle>

            <DialogContent>

                <TextField
                    autoFocus
                    margin="dense"
                    id="username"
                    label="Username"
                    type="text"
                    value={username}
                    onChange={onUsernameChange}
                    onKeyDown={handleKey}
                    fullWidth />

                <TextField
                    margin="dense"
                    id="password"
                    label="Password"
                    type="password"
                    value={password}
                    onChange={onPasswordChange}
                    onKeyDown={handleKey}
                    fullWidth />

            </DialogContent>

            <DialogActions>

                {isLoginFailed && <div className="error-message">Unable to login, please try again!</div>}

                <Button
                    onClick={onLogin}
                    disabled={isLoggingIn || !username || !password}
                    color="primary">

                    {isLoggingIn && <CircularProgress size={20}/>}
                    {isLoggingIn && <span>&nbsp;</span>}
                    Login

                </Button>

            </DialogActions>
        </Dialog>
    );
};

LoginDialog.propTypes = {
    username: PropTypes.string,
    password: PropTypes.string,
    onUsernameChange: PropTypes.func.isRequired,
    onPasswordChange: PropTypes.func.isRequired,
    onLogin: PropTypes.func.isRequired,
    isLoggingIn: PropTypes.bool,
    isLoginFailed: PropTypes.bool,
};

export default LoginDialog;
