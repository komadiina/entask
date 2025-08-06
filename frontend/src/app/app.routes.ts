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
