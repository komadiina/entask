import { Component } from '@angular/core';
import { AuthService } from '@entask-services/auth.service';

@Component({
	selector: 'app-logout-callback',
	template: '',
	imports: [],
	providers: [],
	standalone: true,
})
export class LogoutCallbackComponent {
	constructor(private authService: AuthService) {
		this.authService.logout();
	}
}
