import React from 'react';
import { AppBar, Toolbar, Typography } from '@mui/material';

const TopBar = () => {
		return (
				<AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
					<Toolbar>
						<Typography variant="h6" noWrap component="div">
							Flask License Manager
						</Typography>
					</Toolbar>
				</AppBar>
		);
};

export default TopBar;
