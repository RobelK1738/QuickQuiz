import React, { useEffect, useState } from "react";
import { loginWithGoogle, logout } from "../firebase";
import { Link } from "react-router-dom";

function Navbar() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const savedUser = localStorage.getItem("user");
    if (savedUser) setUser(JSON.parse(savedUser));
  }, []);

  const handleLogin = async () => {
    const signedInUser = await loginWithGoogle();
    if (signedInUser) setUser(signedInUser);
  };

  const handleLogout = async () => {
    await logout();
    setUser(null);
  };

  return (
    <nav className="bg-blue-600 text-white px-6 py-3 shadow-md flex justify-between items-center">
      <h1 className="text-2xl font-bold tracking-wide">
        <Link to="/">QuickQuiz</Link>
      </h1>
      <div className="flex items-center space-x-4">
        <Link to="/" className="hover:text-gray-200">Home</Link>
        <Link to="/my-results" className="hover:text-gray-200">My Results</Link>
        {user ? (
          <>
            <img
              src={user.photoURL}
              alt="profile"
              className="w-8 h-8 rounded-full border-2 border-white"
            />
            <button
              onClick={handleLogout}
              className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded"
            >
              Logout
            </button>
            <Link to="/my-quizzes" className="hover:text-gray-200">My Quizzes</Link>
          </>
        ) : (
          <button
            onClick={handleLogin}
            className="bg-green-500 hover:bg-green-600 px-3 py-1 rounded"
          >
            Login with Google
          </button>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
