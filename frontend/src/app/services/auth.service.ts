import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { LogLevel } from '@entask-constants/logger.constants';
import { KLocalStorage } from '@entask-types/local-storage/local-storage.type';
import { ApiUtil } from '@entask-utilities/api/api.util';
import { LoginResponse } from '@entask-models/login/login-response.model';
import { LocalStorageService } from '@entask-services/local-storage.service';
import { LoggerService } from '@entask-services/logger.service';
import { RedirectService } from '@entask-services/redirect.service';
import { loginObservers } from '@entask-utils/rxjs/observers/login/login.observer';

@Injectable({
	providedIn: 'root',
})
export class AuthService {
	constructor(
		private redirectService: RedirectService,
		private logService: LoggerService,
		private httpClient: HttpClient,
		private localStorageService: LocalStorageService,
	) {
		logService.init({ logLevel: LogLevel.DEBUG, logPrefix: 'AuthService' });

		if (this.isLoggedIn() == false) {
			this.redirectService.redirect({ path: '/login' });
		}
	}

	/**
	 *
	 * @deprecated JWT verification has been implemented on backend, this just provides an additional, minimal layer of security
	 */
	public isLoggedIn(): boolean {
		return this.localStorageService.get('accessToken' as KLocalStorage) != null;
	}

	public login(usernameEmail: string, password: string): void {
		this.logService.log([usernameEmail, password]);
		this.httpClient
			.post<LoginResponse>(ApiUtil.buildUrl('/auth/login'), {
				usernameEmail,
				password,
			})
			.subscribe(loginObservers.loginSubmit);
	}

	public async signupGoogle(): Promise<void> {
		const uri = ApiUtil.buildUrl('/auth/oauth2');
		this.redirectService.absoluteRedirect(uri);
	}
}
