import * as React from 'react';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import TopBar from './components/TopBar';

const darkTheme = createTheme({
  palette: {
	mode: 'dark',
	primary: {
	  main: '#1976d2',
	},
  },
});

export default function App() {

  return (
	<ThemeProvider theme={darkTheme}>
		<Box sx={{ display: 'flex' }}>
			<CssBaseline />
			<TopBar />
			<Box component="main" sx={{ flexGrow: 1, p: 3 }}>
				<Toolbar />
			</Box>
		</Box>
	</ThemeProvider>
  );
}
