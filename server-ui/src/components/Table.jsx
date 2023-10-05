import React, { useState } from 'react';
import { IconButton, Button, TextField, Dialog, DialogActions, DialogContent, Stack, DialogTitle, Box } from '@mui/material';
import { MaterialReactTable } from 'material-react-table';
import { Refresh as RefreshIcon, Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import API from '../Api';
import Toast from './Toast'

export const Table = ({ licenses, setDatabase }) => {

	const [buttonDisable, setButttonDisable] = useState(false);
	const [createNewOpen, setCreateNewOpen] = useState(false);
	const [columnsArray, setColumnsArray] = useState([]);
	const [toastErrorOpen, setToastErrorOpen] = useState(false);
	const [toastErrorMessage, setToastErrorMessage] = useState();
	const [toastSuccessOpen, setToastSuccessOpen] = useState(true);
	const [toastSuccessMessage, setToastSuccessMessage] = useState('Successfully retrieved the database');

	const columns = Object.keys(licenses[0]).map((key)=>{
		return {
			accessorKey: key,
			header: key
		}
	});
  
	const handleToastClose = (reason) => {
		if (reason === 'clickaway') {
			return;
		}
		setToastErrorOpen(false);
		setToastSuccessOpen(false);
	};

	return (
		<>	
			<MaterialReactTable 
				columns={columns}
				data={licenses}
				enableRowActions
				enableColumnActions={false}
				renderRowActions={({ row }) => {

					const handleDelete = async () => {
						setButttonDisable(true);
						await API.delete('/delete', {params:{_id: row.original._id}})
							.then(function (response){
								licenses.splice(row.index, 1);
								setDatabase([...licenses]);
								setToastSuccessMessage(response.data.message);
								setToastSuccessOpen(true);
							})
							.catch(function (error){
								if (error.response){
									setToastErrorMessage(error.response.data.message);
									setToastErrorOpen(true);
								} else if (error.request) {
									console.error(error.request);
								} else {
									console.error('Error', error.message);
								}
							});
						await setButttonDisable(false);
					};

					return(
						<Box sx={{ display: 'flex', flexWrap: 'nowrap' }}>
							<IconButton
								color="error"
								onClick={handleDelete}
								disabled={buttonDisable}
							>
								<DeleteIcon />
							</IconButton>
						</Box>
				  	);
				}}
				renderTopToolbarCustomActions={() => {
			
					const handleRefresh = async () => {
						setButttonDisable(true);
						await API.get('/get-all')
							.then(function (response){
								setDatabase(response.data['license-database']);
								setToastSuccessMessage('Successfully refreshed the database');
								setToastSuccessOpen(true);
							})
							.catch(function (error){
								if (error.response){
									setToastErrorMessage(error.response.data.message);
									setToastErrorOpen(true);
								} else if (error.request) {
									console.error(error.request);
								} else {
									console.error('Error', error.message);
								}
							});
						await setButttonDisable(false);
					};

					const handleOpenDialog = async() => {
						setButttonDisable(true);
						await API.get('/create-fields')
							.then(function (response){
								setColumnsArray(response.data['fields']);
								setCreateNewOpen(true);
							})
							.catch(function (error){
								if (error.response){
									setToastErrorMessage(error.response.data.message);
									setToastErrorOpen(true);
								} else if (error.request) {
									console.error(error.request);
								} else {
									console.error('Error', error.message);
								}
							});
						await setButttonDisable(false);
					}

					const handleCreate = async(values) => {
						await API.post('/create', values)
							.then(function (response){
								setToastSuccessMessage(response.data.message);
								setToastSuccessOpen(true);
								handleRefresh();
							})
							.catch(function (error){
								if (error.response){
									setToastErrorMessage(error.response.data.message);
									setToastErrorOpen(true);
								} else if (error.request) {
									console.error(error.request);
								} else {
									console.error('Error', error.message);
								}
							});
					}
			
					return (
					  <div style={{ display: 'flex', gap: '0.5rem' }}>
						<IconButton
							onClick={handleRefresh}
							disabled={buttonDisable}
						>
							<RefreshIcon />
						</IconButton>
						<IconButton
							onClick={handleOpenDialog}
							disabled={buttonDisable}
						>
							<AddIcon />
						</IconButton>
						<CreateNewLicenseWindow
							columns={columnsArray}
							open={createNewOpen}
							onClose={() => setCreateNewOpen(false)}
							onSubmit={handleCreate}
						/>
					  </div>
					);
				}}
			/>
			<Toast open={toastErrorOpen} toastMessage={toastErrorMessage} toastSeverity='error' handleClose={handleToastClose} />
			<Toast open={toastSuccessOpen} toastMessage={toastSuccessMessage} toastSeverity='success' handleClose={handleToastClose} />
		</>
	);
};

export const CreateNewLicenseWindow = ({ open, columns, onClose, onSubmit }) => {
	const [values, setValues] = useState(() =>
		columns.reduce((acc, column) => {
			acc[column ?? ''] = '';
			return acc;
		}, {}),
	);
  
	const handleSubmit = async () => {
		onSubmit(values);
		setValues({})
		onClose();
	};
  
	return (
	  <Dialog open={open}>
		<DialogTitle textAlign="center">Create New License</DialogTitle>
		<DialogContent>
			<Stack
				sx={{
				width: '100%',
				minWidth: { xs: '300px', sm: '360px', md: '400px' },
				gap: '1.5rem',
				}}
			>
			  {columns.map((column) => (
				<TextField
					key={column}
					label={column}
					name={column}
					onChange={(e) =>
						setValues({ ...values, [e.target.name]: e.target.value })
					}
					required
				/>
			  ))}
			</Stack>
		</DialogContent>
		<DialogActions sx={{ p: '1.25rem' }}>
			<Button onClick={onClose}>Cancel</Button>
			<Button color="primary" onClick={handleSubmit} variant="contained">Create</Button>
		</DialogActions>
	  </Dialog>
	);
  };

export default Table;
