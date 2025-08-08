import { Routes } from '@angular/router';
import { AuthGuard } from './utilities/auth/auth-guard.guard';

export const routes: Routes = [
	{
		path: '',
		pathMatch: 'full',
		redirectTo: '/login',
	},
	{
		path: 'login',
		pathMatch: 'full',
		loadComponent: () =>
			import('@entask-pages/login/login.component').then(
				(c) => c.LoginComponent,
			),
		title: 'Entask | Login',
	},
	{
		path: 'register',
		pathMatch: 'full',
		loadComponent: () =>
			import('@entask-pages/register/register.component').then(
				(c) => c.RegisterComponent,
			),
		title: 'Entask | Register',
	},
	{
		path: 'forgotten-password',
		pathMatch: 'full',
		loadComponent: () =>
			import(
				'@entask-pages/forgotten-password/forgotten-password.component'
			).then((c) => c.ForgottenPasswordComponent),
		title: 'Entask | Reset password',
	},
	{
		path: 'profile',
		pathMatch: 'full',
		loadComponent: () =>
			import('@entask-pages/profile/profile.component').then(
				(c) => c.ProfileComponent,
			),
		canActivate: [AuthGuard],
		title: 'Entask | Profile',
	},
	{
		path: 'dashboard',
		pathMatch: 'full',
		loadComponent: () =>
			import('@entask-pages/dashboard/dashboard.component').then(
				(c) => c.DashboardComponent,
			),
		canActivate: [AuthGuard],
		title: 'Entask | Dashboard',
	},
	{
		path: '**',
		redirectTo: '/login',
	},
];
