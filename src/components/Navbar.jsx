import React from "react";
import "./Navbar.css";
import { useAuth0 } from "@auth0/auth0-react";

const Navbar = () => {
  const { user, loginWithRedirect, logout } = useAuth0();
  console.log(user);
  console.log("Gautam")
  return (
    <div className="navbar-container">

      <span>
        <span className="logo">
          <img className="logo" src={process.env.PUBLIC_URL + '/bot.png'} alt="" srcset="" />
        </span>

        <span className="company-name">PictoPixie</span>
      </span>

      <span className="user">
        {
          user ? (<img src={user.picture} alt="user-picture" onClick={user ? loginWithRedirect : logout} />) : (<i class="fa-solid fa-user" onClick={user ? loginWithRedirect : logout}></i>)
        }
      </span>

    </div>
  );
};

export default Navbar;
