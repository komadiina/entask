import { HttpClient } from '@angular/common/http';
import { EnvironmentInjector, Injectable } from '@angular/core';
import { Observer } from 'rxjs';
import { LogLevel } from '@entask-root/constants/logger.constants';
import { LoggerService } from '@entask-root/services/logger.service';
import { environment } from '@entask-environments/environment';
import { RedirectService } from './redirect.service';

@Injectable({
	providedIn: 'root',
})
export class AuthService {
	constructor(
		private redirectService: RedirectService,
		private logService: LoggerService,
		private envInjector: EnvironmentInjector,
		private httpClient: HttpClient,
	) {
		logService.init({ logLevel: LogLevel.DEBUG, logPrefix: 'AuthService' });

		if (this.isLoggedIn() == false) {
			this.redirectService.redirect({ path: '/login' });
		}
	}

	public isLoggedIn(): boolean {
		return localStorage.getItem('token') ? true : false;
	}

	public login(username: string, password: string): void {
		this.logService.log([username, password]);
	}

	public async signupGoogle(): Promise<void> {
		const observer: Observer<object> = {
			next: (res) => {
				console.log(res);
			},
			complete: () => {
				console.log('complete');
			},
			error: (err) => {
				console.log(err);
			},
		};

		this.httpClient
			.post(environment.backendUrl + '/auth/google', {})
			.subscribe(observer);
	}
}
