// src/App.js
import React, { useState, useEffect } from "react";
import Register from "./components/Register";
import Login from "./components/Login";
import Assistant from "./components/Assistant";

const App = () => {
	const [token, setToken] = useState(
		localStorage.getItem("access_token") || ""
	);
	const [user, setUser] = useState(null);
	const [showRegister, setShowRegister] = useState(false);

	useEffect(() => {
		if (token) {
			fetch(`${process.env.REACT_APP_API_URL}/api/users/me`, {
				headers: {
					Authorization: `Bearer ${token}`,
				},
			})
				.then((response) => response.json())
				.then((data) => {
					setUser(data);
				});
		}
	}, [token]);

	const handleLoginSuccess = (receivedToken) => {
		setToken(receivedToken);
		// call API to get current user
		fetch(`${process.env.REACT_APP_API_URL}/api/users/me`, {
			headers: {
				Authorization: `Bearer ${receivedToken}`,
			},
		})
			.then((response) => response.json())
			.then((data) => {
				setUser(data);
			});
	};

	const handleRegisterSuccess = () => {
		setShowRegister(false);
	};

	const handleLogout = () => {
		setToken("");
	};

	const switchToRegister = () => {
		setShowRegister(true);
	};

	const switchToLogin = () => {
		setShowRegister(false);
	};

	if (!token) {
		return showRegister ? (
			<Register
				onRegisterSuccess={handleRegisterSuccess}
				switchToLogin={switchToLogin}
			/>
		) : (
			<Login
				onLoginSuccess={handleLoginSuccess}
				switchToRegister={switchToRegister}
			/>
		);
	}

	return <Assistant token={token} onLogout={handleLogout} user={user} />;
};

export default App;
