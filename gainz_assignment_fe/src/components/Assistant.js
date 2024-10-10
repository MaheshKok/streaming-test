// src/components/Assistant.js
import React, { useState, useEffect, useRef } from "react";
import {
	AppBar,
	Toolbar,
	Typography,
	CssBaseline,
	Container,
	Box,
	TextField,
	Button,
	Select,
	MenuItem,
	FormControl,
	InputLabel,
	CircularProgress,
} from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";
import theme from "./Theme";
import { marked } from "marked";

import LogoutIcon from "@mui/icons-material/Logout"; // Import the icon

const Assistant = ({ token, onLogout, user }) => {
	const [messages, setMessages] = useState([]);
	const [inputValue, setInputValue] = useState("");
	const [loading, setLoading] = useState(false);
	const wsRef = useRef(null);
	const [threads, setThreads] = useState([]);
	const [currentThreadId, setCurrentThreadId] = useState(null);
	const [assistants, setAstAssistantss] = useState([]);
	const [currentAssistantId, setsetCurrentAssistantId] = useState(null);
	const [wsConnected, setWsConnected] = useState(false);

	useEffect(() => {
		// Fetch all threads when the component mounts
		fetch(`${process.env.REACT_APP_API_URL}/api/threads?token=${token}`)
			.then((response) => response.json())
			.then((data) => {
				const threadIds = data.map((item) => item.openai_thread_id);
				setThreads(threadIds);
			})
			.catch((error) => {
				console.error("Error fetching threads:", error);
			});
	}, [token]);

	useEffect(() => {
		// Fetch all threads when the component mounts
		fetch(`${process.env.REACT_APP_API_URL}/api/assistants?token=${token}`)
			.then((response) => response.json())
			.then((data) => {
				const assistantIds = data.map((item) => item.openai_assistant_id);
				setAstAssistantss(assistantIds);
				setsetCurrentAssistantId(assistantIds[0]);
			})
			.catch((error) => {
				console.error("Error fetching assistants:", error);
			});
	}, [token]);

	useEffect(() => {
		if (currentThreadId) {
			connectWebSocket(currentThreadId);
		}

		// Cleanup function to close WebSocket when component unmounts or thread changes
		return () => {
			if (wsRef.current) {
				wsRef.current.close();
				wsRef.current = null;
			}
		};
	}, [currentThreadId]);

	const connectWebSocket = (threadId) => {
		// Close existing WebSocket connection if any
		if (wsRef.current) {
			wsRef.current.close();
		}

		const websocket = new WebSocket(
			`${process.env.REACT_APP_WS_URL}/api/assistants/ws?token=${token}&thread_id=${threadId}&assistant_id=${currentAssistantId}`
		);

		websocket.onopen = () => {
			console.log("WebSocket connection established");
			wsRef.current = websocket;
			setWsConnected(true);
		};

		websocket.onmessage = (event) => {
			setLoading(false);
			const data = event.data;
			setMessages((prevMessages) => {
				const lastMessage = prevMessages[prevMessages.length - 1];
				if (
					lastMessage &&
					lastMessage.role === "assistant" &&
					!lastMessage.isComplete
				) {
					// Update the last assistant message
					const updatedMessage = {
						...lastMessage,
						content: lastMessage.content + data,
					};
					return [...prevMessages.slice(0, -1), updatedMessage];
				} else {
					// Add new assistant message
					return [
						...prevMessages,
						{
							role: "assistant",
							content: data,
							isComplete: false,
						},
					];
				}
			});
		};

		websocket.onclose = (event) => {
			console.log(
				`WebSocket connection closed: code=${event.code}, reason=${event.reason}`
			);
			wsRef.current = null;
			setWsConnected(false);
		};

		websocket.onerror = (error) => {
			console.error("WebSocket error:", error);
		};
	};

	const handleCreateNew = () => {
		fetch(`${process.env.REACT_APP_API_URL}/api/threads?token=${token}`, {
			method: "POST",
		})
			.then((response) => response.json())
			.then((data) => {
				console.log(`threads: ${JSON.stringify(data)}`);
				const newThreadId = data.openai_thread_id;
				setThreads([...threads, newThreadId]);
				setCurrentThreadId(newThreadId);
				setMessages([]);
			})
			.catch((error) => {
				console.error("Error creating new thread:", error);
			});
	};

	const handleSelectThread = (event) => {
		const threadId = event.target.value;
		setCurrentThreadId(threadId);
		setMessages([]);
	};

	const handleSelectAssistant = (event) => {
		const assistantId = event.target.value;
		setsetCurrentAssistantId(assistantId);
		setMessages([]);
	};

	const handleSend = () => {
		if (
			!loading &&
			inputValue.trim() !== "" &&
			wsConnected &&
			wsRef.current &&
			wsRef.current.readyState === WebSocket.OPEN
		) {
			setMessages((prevMessages) => [
				...prevMessages,
				{ role: "user", content: inputValue },
			]);
			wsRef.current.send(inputValue);
			setInputValue("");
			setLoading(true);
		} else {
			console.error("WebSocket is not open. Unable to send message.");
		}
	};

	const handleLogout = () => {
		if (wsRef.current) {
			wsRef.current.close();
			wsRef.current = null;
		}
		localStorage.removeItem("access_token");
		onLogout();
	};

	return (
		<ThemeProvider theme={theme}>
			<CssBaseline />
			<Container maxWidth="md">
				<AppBar position="static">
					<Toolbar>
						<Typography variant="h6">AI Assistant 🤓</Typography>
						<Box sx={{ flexGrow: 1 }} />
						<Box mr="10">{user?.email}</Box>
						<Box sx={{ flexGrow: 0.1 }} />
						<Button
							color="secondary"
							variant="contained"
							startIcon={<LogoutIcon />}
							onClick={handleLogout}
						>
							Logout
						</Button>
					</Toolbar>
				</AppBar>
				<Box sx={{ my: 4 }}>
					<FormControl fullWidth sx={{ mb: 4 }}>
						<InputLabel id="thread-select-label">Select Thread</InputLabel>
						<Select
							labelId="thread-select-label"
							value={currentThreadId || ""}
							label="Select Thread"
							onChange={handleSelectThread}
						>
							{threads &&
								threads.map((threadId) => (
									<MenuItem key={threadId} value={threadId}>
										{threadId}
									</MenuItem>
								))}
						</Select>
						<Button
							variant="contained"
							color="primary"
							onClick={handleCreateNew}
							sx={{ mt: 2 }}
						>
							Create New Thread
						</Button>
					</FormControl>
					<FormControl fullWidth>
						<InputLabel id="assistant-select-label">
							Select Assistant
						</InputLabel>
						<Select
							labelId="assistant-select-label"
							value={currentAssistantId || ""}
							label="Select Assistant"
							onChange={handleSelectAssistant}
						>
							{assistants &&
								assistants.map((assistantId) => (
									<MenuItem key={assistantId} value={assistantId}>
										{assistantId}
									</MenuItem>
								))}
						</Select>
					</FormControl>
					<Box sx={{ mt: 4 }}>
						{messages.map((msg, index) => (
							<Box key={index} sx={{ mb: 2 }}>
								<Typography variant="body1" color="textSecondary">
									{msg.role === "user" ? "You" : "Assistant"}
								</Typography>
								<Box
									sx={{
										p: 2,
										bgcolor:
											msg.role === "user" ? "primary.main" : "secondary.main",
										borderRadius: 1,
									}}
									dangerouslySetInnerHTML={{
										__html: marked.parse(msg.content),
									}}
								/>
							</Box>
						))}
						{loading && (
							<Box display="flex" justifyContent="center" my={4}>
								<CircularProgress />
							</Box>
						)}
					</Box>
					<Box sx={{ display: "flex", mt: 2 }}>
						<TextField
							fullWidth
							variant="outlined"
							placeholder="Type your message..."
							value={inputValue}
							onChange={(e) => setInputValue(e.target.value)}
							onKeyPress={(e) => {
								if (e.key === "Enter") {
									handleSend();
								}
							}}
						/>
						<Button
							variant="contained"
							color="primary"
							onClick={handleSend}
							disabled={loading || !wsConnected}
							sx={{ ml: 2 }}
						>
							Send
						</Button>
					</Box>
				</Box>
			</Container>
		</ThemeProvider>
	);
};

export default Assistant;
