import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { LocalStorageService } from '@entask-root/services/local-storage.service';

@Component({
	imports: [],
	providers: [],
	template: '',
	standalone: true,
})
export class OAuth2CallbackComponent {
	constructor(
		private route: ActivatedRoute,
		private router: Router,
		private localStorageService: LocalStorageService,
	) {
		this.route.queryParams.subscribe((params) => {
			const accessToken = params['access_token'];
			const refreshToken = params['refresh_token'];
			const idToken = params['id_token'];

			this.localStorageService.updateMany({
				idToken,
				accessToken,
				refreshToken,
			});

			this.router.navigate(['/dashboard']);
		});
	}
}
