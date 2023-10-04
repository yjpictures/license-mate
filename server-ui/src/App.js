import React, { useState, useMemo } from 'react';
import { Box, CssBaseline, useMediaQuery } from '@mui/material';;
import { ThemeProvider, createTheme } from '@mui/material/styles';
import SignInSide from './views/NotLoggedIn';
import RegularView from './views/LoggedIn';

export default function App() {

	const [password, setPassword] = useState();
	const [database, setDatabase] = useState([{}]);
	const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
	const theme = useMemo(
		() =>
		createTheme({
			palette: {
			mode: prefersDarkMode ? 'dark' : 'light',
			},
		}),
		[prefersDarkMode],
	);

	return (
		<ThemeProvider theme={theme}>
			<Box sx={{ display: 'flex' }}>
				<CssBaseline />	
				{ password === null || password === undefined
					?	<SignInSide setPassword={setPassword} setDatabase={setDatabase} />
					:	<RegularView setPassword={setPassword} database={database} setDatabase={setDatabase} />
				}
			</Box>
		</ThemeProvider>
	);
}
