// src/components/Register.js
import React, { useState } from "react";
import { Container, Box, Typography, TextField, Button } from "@mui/material";

const Register = ({ onRegisterSuccess, switchToLogin }) => {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [message, setMessage] = useState("");

	const handleRegister = async () => {
		try {
			const response = await fetch(
				`${process.env.REACT_APP_API_URL}/api/auth/register`,
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({ email, password }),
				}
			);

			if (response.ok) {
				setMessage("Registration successful! Please log in.");
				onRegisterSuccess();
			} else {
				const data = await response.json();
				setMessage(data.detail || "Registration failed.");
			}
		} catch (error) {
			setMessage("An error occurred during registration.");
		}
	};

	return (
		<Container maxWidth="sm">
			<Box my={4}>
				<Typography variant="h4" gutterBottom>
					Register
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
					<Button variant="contained" color="primary" onClick={handleRegister}>
						Register
					</Button>
					<Button
						variant="text"
						color="secondary"
						onClick={switchToLogin}
						style={{ marginLeft: "8px" }}
					>
						Back to Login
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

export default Register;
