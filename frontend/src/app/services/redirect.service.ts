import { Injectable } from '@angular/core';
import { Route } from '@angular/router';

@Injectable({
	providedIn: 'root',
})
export class RedirectService {
	public redirect(destination: Route, replace = false): void {
		if (window.location.pathname != destination.path) {
			if (replace) {
				window.location.replace(destination.path!);
			} else {
				window.location.assign(destination.path!);
			}
		}
	}

	public absoluteRedirect(uri: string): void {
		window.location.href = uri;
	}
}
