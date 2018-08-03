import App from './App/App'; 
import Auth from './Auth/Auth'; 
import Base from './Base/Base';
import LoginPage from './Login/LoginPage'; 
import SignUpPage from './SignUp/SignUpPage';
import AboutUs from './AboutUs/AboutUs';

const routes = {
    component: Base,
    childRoutes: [
        {
            path: '/',
            getComponent: (location, callback) => {
                if (Auth.isUserAuthenticated()) {
                    // if login, show App component
                    callback(null, App);
                } else {
                    // otherwise, show LoginPage
                    callback(null, LoginPage);
                } 
            }
        },

        {
            path: '/login',
            component: LoginPage
        },

        {
            path: '/signup',
            component: SignUpPage
        },

        {
            path: '/logout',
            onEnter: (nextState, replace) => {
            // logout remove token
              Auth.deauthenticateUser();
            // redireact to root, then redireact to LoginPage
              replace('/');
            }
        },

        {
            path: '/aboutus',
            component: AboutUs
        },
    ]
}

export default routes;
