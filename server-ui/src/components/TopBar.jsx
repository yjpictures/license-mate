import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';

export const TopBar = ({ setPassword }) => {
		return (
			<AppBar>
				<Toolbar>
					<Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
						Flask License Manager
					</Typography>
					<Button color="inherit" onClick={() => setPassword(null)}>Logout</Button>
				</Toolbar>
			</AppBar>
		);
};

export default TopBar;
