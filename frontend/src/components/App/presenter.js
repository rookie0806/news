import React from "react";
import PropTypes from "prop-types";
import "./styles.scss";
import Footer from "components/Footer";
import {Route, Switch} from "react-router-dom"; 
import Auth from "components/Auth";
import Navigation from "components/Navigation";
import Main from "components/Main";
import Logout from "components/Logout";
import Delete from "components/DeleteForm";
const App = props => [
    //Nav,
    //Router,
    <Navigation key={1}/> ,
    props.isLoggedIn ? <PrivateRoutes key={2}/> : <PublicRoutes key={2}/>, //priv :public 
    //<PublicRoutes key={2}/>,
    <Footer key={3} />
];

App.propTypes = {
    isLoggedIn: PropTypes.bool.isRequired
}
const PrivateRoutes = props => (
    <Switch>
        <Route path="/" component={Main}/>
    </Switch>
)

const PublicRoutes = props => (
    <Switch>
        <Route path="/" component={Main}/>
    </Switch>
)   
export default App;
