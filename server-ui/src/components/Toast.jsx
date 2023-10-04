import React, { useState } from 'react';
import { Snackbar, Alert } from '@mui/material';

export default function Toast({ toastMessage, toastSeverity }) {

	const [open, setOpen] = useState(true);
  
	const handleClose = (reason) => {
		if (reason === 'clickaway') {
			return;
		}
		setOpen(false);
	};
  
	return (
		<Snackbar open={open} autoHideDuration={2000} onClose={handleClose}>
			<Alert onClose={handleClose} variant="filled" severity={toastSeverity} sx={{ width: '100%' }}>
				{toastMessage}
			</Alert>
		</Snackbar>
	);
}
