import { Injectable } from '@angular/core';
import { Route } from '@angular/router';

@Injectable({
	providedIn: 'root',
})
export class RedirectService {
	public redirect(destination: Route): void {
		if (window.location.pathname != destination.path) {
			window.location.replace(destination.path!);
		}
	}
}
