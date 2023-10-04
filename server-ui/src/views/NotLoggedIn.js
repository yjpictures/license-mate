import React, { useState } from 'react';
import { Avatar, Button, TextField, Paper, Box, Grid, Typography, LinearProgress, Alert } from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import API from '../Api';

export default function SignInSide({ setPassword, setDatabase }) {

	const handleSubmit = async (event) => {
		setAlertText(null)
		event.preventDefault();
		const data = new FormData(event.currentTarget);
		if (data.get('password') != null && data.get('password').trim() != '') {
			setButttonDisable(true);
			API.defaults.headers.common['Authorization'] = 'Basic ' + btoa('admin:' + await data.get('password'));
			await API.get('/get-all')
				.then(function(response){
					setDatabase(response.data['license-database']);
					setPassword(data.get('password'));
				})
				.catch(function (error){
					if (error.response){
						setAlertText(error.response.data.message);
					} else if (error.request) {
						console.error(error.request);
					} else {
						console.error('Error', error.message);
					}
				});
			await setButttonDisable(false);
		} else {
			setAlertText('Empty Password')
		}
	};

	const [buttonDisable, setButttonDisable] = useState(false);
	const [alertText, setAlertText] = useState(null);

	return (
		<Grid container component="main" sx={{ height: '100vh' }}>
			<Grid
				item
				xs={false}
				sm={4}
				md={7}
				sx={{
					backgroundImage: 'url(https://source.unsplash.com/random?wallpapers)',
					backgroundRepeat: 'no-repeat',
					backgroundColor: (t) =>
						t.palette.mode === 'light' ? t.palette.grey[50] : t.palette.grey[900],
					backgroundSize: 'cover',
					backgroundPosition: 'center',
				}}
			/>
			<Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
				<Box
					sx={{
						my: 8,
						mx: 4,
						display: 'flex',
						flexDirection: 'column',
						alignItems: 'center',
					}}
				>
					<Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
						<LockOutlinedIcon />
					</Avatar>
					<Typography component="h1" variant="h5">
						Flask License Manager | Admin
					</Typography>
					<Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="user"
							label="User"
							name="user"
							autoComplete="user"
							autoFocus
							value="admin"
						/>
						<TextField
							margin="normal"
							required
							fullWidth
							name="password"
							label="Password"
							type="password"
							id="password"
							autoComplete="current-password"
							autoFocus
						/>
						{buttonDisable
							? <LinearProgress/>
							: null
						}
						<Button
							type="submit"
							fullWidth
							variant="contained"
							sx={{ mt: 3, mb: 2 }}
							disabled={buttonDisable}
						>
							Sign In
						</Button>
						{alertText != null && alertText != ''
							? <Alert variant="filled" severity="error"> {alertText} </Alert>
							: null
						}
					</Box>
				</Box>
			</Grid>
		</Grid>
	);
}
