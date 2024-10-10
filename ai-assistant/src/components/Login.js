// src/components/Login.js
import React, { useState } from "react";
import { Container, Box, Typography, TextField, Button } from "@mui/material";

const Login = ({ onLoginSuccess, switchToRegister }) => {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [message, setMessage] = useState("");

	const handleLogin = async () => {
		try {
			const response = await fetch(
				`${process.env.REACT_APP_API_URL}/api/auth/jwt/login`,
				{
					method: "POST",
					headers: {
						"Content-Type": "application/x-www-form-urlencoded",
					},
					body: new URLSearchParams({
						username: email,
						password: password,
					}),
				}
			);

			if (response.ok) {
				const data = await response.json();
				const token = data.access_token;
				localStorage.setItem("access_token", token);
				setMessage("Login successful!");
				onLoginSuccess(token);
			} else {
				const data = await response.json();
				setMessage(data.detail || "Login failed.");
			}
		} catch (error) {
			setMessage("An error occurred during login.");
		}
	};

	return (
		<Container maxWidth="sm">
			<Box my={4}>
				<Typography variant="h4" gutterBottom>
					Login
				</Typography>
				<TextField
					label="Email"
					variant="outlined"
					fullWidth
					margin="normal"
					value={email}
					onChange={(e) => setEmail(e.target.value)}
				/>
				<TextField
					label="Password"
					type="password"
					variant="outlined"
					fullWidth
					margin="normal"
					value={password}
					onChange={(e) => setPassword(e.target.value)}
				/>
				<Box display="flex" alignItems="center" mt={2}>
					<Button variant="contained" color="primary" onClick={handleLogin}>
						Login
					</Button>
					<Button
						variant="text"
						color="secondary"
						onClick={switchToRegister}
						style={{ marginLeft: "8px" }}
					>
						Register
					</Button>
				</Box>
				{message && (
					<Typography color="error" variant="body2" mt={2}>
						{message}
					</Typography>
				)}
			</Box>
		</Container>
	);
};

export default Login;
