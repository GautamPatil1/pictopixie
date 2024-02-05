import React from "react";
import "./Navbar.css";
import { useAuth0 } from "@auth0/auth0-react";

const Navbar = () => {
  const { isAuthenticated, user, loginWithRedirect, logout } = useAuth0();
  return (
    <div className="navbar-container">

      <span>
        <span className="logo">
          <img className="logo" src={process.env.PUBLIC_URL + '/bot.png'} alt="" srcSet="" />
        </span>

        <span className="company-name">PictoPixie</span>
      </span>

      <span className="user">
        {
          user ? (<img referrerPolicy="no-referrer" src={user.picture} alt="user" onClick={user ? logout : loginWithRedirect} />) : (<i className="fa-solid fa-user" onClick={user ? logout : loginWithRedirect}></i>)
        }
      </span>

    </div>
  );
};

export default Navbar;
