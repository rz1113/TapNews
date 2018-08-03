import React from 'react';
import LoginForm from './LoginForm';
import PropTypes from 'prop-types';
import Auth from '../Auth/Auth';

class LoginPage extends React.Component {
    constructor(props, context) {
        super(props, context);
    
        this.state = {
          errors: {},
          user: {
            email: '',
            password: ''
          }
        };
    }

    changeUser(event) {
        const field = event.target.name;
        const user = this.state.user;
        user[field] = event.target.value;

        this.setState({
            user: user
        });
    }

    processForm(event) {
        event.preventDefault();

        const email = this.state.user.email;
        const password = this.state.user.password;

        console.log('email:', email);
        console.log('password:', password);

        //post login data
        const url = "http://" + window.location.hostname + ":3000" + "/auth/login";
        const request = new Request(
            url,
            {
                method:'POST', headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        )

        //send request
        fetch(request).then(response => {
            if (response.status === 200) {
                // may have error, after login clear the error
                this.setState({ errors:{}});

                response.json().then(json => {
                     console.log(json);
                     // "token" should match with server
                     Auth.authenticateUser(json.token, email);
                     // redireact to root, since client already login, App component will be shown.
                     this.context.router.replace('/');
                });
            } else {
                console.log("Login failed");
                response.json().then(json => {
                    const errors = json.errors ? json.errors : {};
                    errors.summary = json.message;
                    this.setState({errors});
                });
            }
        });
    }

    render() {
        return(
            <LoginForm
                onSubmit={(e) => this.processForm(e)}
                onChange={(e) => this.changeUser(e)}
                errors={this.state.errors}
                user={this.state.user} />
        );
    }
}

LoginPage.contextTypes = {
    router: PropTypes.object.isRequired
}
    

export default LoginPage;