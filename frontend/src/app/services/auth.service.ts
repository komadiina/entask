import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { KLocalStorage } from '@entask-types/local-storage/local-storage.type';
import { ApiUtil } from '@entask-utilities/api/api.util';
import { Subscription } from 'rxjs';
import { LoginComponent } from '@entask-pages/login/login.component';
import { LoginResponse } from '@entask-models/login/login-response.model';
import { LocalStorageService } from '@entask-services/local-storage.service';
import { RedirectService } from '@entask-services/redirect.service';
import { loginObservers } from '@entask-utils/rxjs/observers/login/login.observer';

@Injectable({
	providedIn: 'root',
})
export class AuthService {
	private _hostComponent: LoginComponent | null = null;

	public set hostComponent(c: LoginComponent) {
		this._hostComponent = c;
	}

	constructor(
		private redirectService: RedirectService,
		private httpClient: HttpClient,
		private localStorageService: LocalStorageService,
	) {
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

	public login(usernameEmail: string, password: string): Subscription {
		return this.httpClient
			.post<LoginResponse>(ApiUtil.buildUrl('/auth/login'), {
				usernameEmail,
				password,
			})
			.subscribe(loginObservers.loginSubmit.context(this._hostComponent!));
	}

	public async logout(): Promise<void> {
		this.httpClient.post(ApiUtil.buildUrl('/auth/logout'), {}).subscribe();
		this.localStorageService.clear();
	}

	public async signupGoogle(): Promise<void> {
		const uri = ApiUtil.buildUrl('/auth/oauth2');
		this.redirectService.absoluteRedirect(uri);
	}
}
