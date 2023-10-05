import React from 'react';
import { Box, Toolbar } from '@mui/material';
import TopBar from '../components/TopBar';
import Table from '../components/Table';

export default function RegularView({ setPassword, database, setDatabase }) {

	return (
        <Box sx={{ display: 'flex' }}>
            <TopBar setPassword={setPassword}/>
            <Box component="main" sx={{ flexGrow: 1, p: 3, width: '100vw' }}>
                <Toolbar />
				<Box sx={{ width: '100%' }}>
					<Table licenses={database} setDatabase={setDatabase} />
				</Box>
            </Box>
        </Box>
	);
}
