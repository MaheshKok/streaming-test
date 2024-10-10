import { createTheme } from "@mui/material/styles";
import grey from "@mui/material/colors/grey";
import red from "@mui/material/colors/red";
import green from "@mui/material/colors/green";

const theme = createTheme({
	palette: {
		primary: {
			main: red[300], // Custom Light Red
			contrastText: "#000000", // Text color contrasting with light red
		},
		secondary: {
			main: green[300], // Custom Light Green
			contrastText: "#000000", // Text color contrasting with light green
		},
		background: {
			default: grey[50], // Very light grey background
		},
	},
});

export default theme;
