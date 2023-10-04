import React, { useState } from 'react';
import { IconButton } from '@mui/material';
import { MaterialReactTable } from 'material-react-table';
import { Refresh as RefreshIcon, Add as AddIcon } from '@mui/icons-material';
import API from '../Api';

export const Table = ({ licenses, setDatabase }) => {

	const [buttonDisable, setButttonDisable] = useState(false);

	const columns = Object.keys(licenses[0]).map((key)=>{
		return {
			accessorKey: key,
			header: key
		}
	});

	return (
		<>	
			<h1>Database</h1>
			<MaterialReactTable 
				columns={columns}
				data={licenses}
				enableColumnActions={false}
				renderTopToolbarCustomActions={({ table }) => {
			
					const handleRefresh = async () => {
						setButttonDisable(true);
						await API.get('/get-all')
							.then(function(response){
								setDatabase(response.data['license-database']);
							})
							.catch(function (error){
								if (error.response){
									console.error(error.response.data.message);
								} else if (error.request) {
									console.error(error.request);
								} else {
									console.error('Error', error.message);
								}
							});
						await setButttonDisable(false);
					};

					const handleAdd = async() => {
						setButttonDisable(true);
						console.info('Create a License Feature Coming Soon!');
						await setButttonDisable(false);
					}
			
					return (
					  <div style={{ display: 'flex', gap: '0.5rem' }}>
						<IconButton onClick={handleRefresh} disabled={buttonDisable}>
							<RefreshIcon />
						</IconButton>
						<IconButton onClick={handleAdd} disabled={buttonDisable}>
							<AddIcon />
						</IconButton>
					  </div>
					);
				}}
			/>
		</>
	);
};

export default Table;
