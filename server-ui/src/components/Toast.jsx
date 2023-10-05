import React from 'react';
import { Snackbar, Alert } from '@mui/material';

export default function Toast({ open, toastMessage, toastSeverity, handleClose }) {
	return (
		<Snackbar open={open} autoHideDuration={5000} onClose={handleClose}>
			<Alert onClose={handleClose} variant="filled" severity={toastSeverity} sx={{ width: '100%' }}>
				{toastMessage}
			</Alert>
		</Snackbar>
	);
}
