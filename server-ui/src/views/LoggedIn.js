import React from 'react';
import { Box, Toolbar } from '@mui/material';
import TopBar from '../components/TopBar';
import Table from '../components/Table';

export default function RegularView({ setPassword, database, setDatabase }) {

	return (
        <Box sx={{ display: 'flex' }}>
            <TopBar setPassword={setPassword}/>
            <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
                <Toolbar />
				<Box sx={{ width: '90vw' }}>
					<Table licenses={database} setDatabase={setDatabase} />
				</Box>
            </Box>
        </Box>
	);
}
