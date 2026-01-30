import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="logo">
        <Link to="/">FashionStore</Link>
      </div>
      <ul className="nav-links">
        <li><Link to="/products">Products</Link></li>
        <li><Link to="/feedback">Feedback</Link></li>
        <li><Link to="/signin">Sign In</Link></li>
        <li><Link to="/register">Register</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
