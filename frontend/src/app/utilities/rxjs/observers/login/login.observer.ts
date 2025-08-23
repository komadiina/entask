import { BaseObserver } from '@entask-utilities/rxjs/observers/base.observer';
import { LoginComponent } from '@entask-pages/login/login.component';
import { LoginResponse } from '@entask-models/login/login-response.model';
import { LocalStorageService } from '@entask-services/local-storage.service';

export const loginObservers = {
	loginSubmit: new BaseObserver<LoginResponse, LoginComponent>(
		(value: LoginResponse, ctx?: LoginComponent | null): void => {
			LocalStorageService.set('accessToken', value.accessToken);
			LocalStorageService.set('refreshToken', value.refreshToken);
			LocalStorageService.set('idToken', value.idToken);
			LocalStorageService.set('authProvider', value.provider);
			LocalStorageService.set('tokenType', value.tokenType);

			if (ctx) {
				ctx.getMessageService.add({
					severity: 'success',
					summary: 'Success',
					detail: 'Login successful.',
				});

				ctx.redirectService.redirect({ path: '/dashboard' }, false);
			}
		},

		(error: Error, ctx?: LoginComponent | null): void => {
			console.error(error);

			if (ctx) {
				ctx.getMessageService.add({
					severity: 'error',
					summary: 'Error',
					detail: error.message ?? 'Invalid credentials supplied.',
				});
			}
		},

		(): void => {
			// noop
		},
	),
};
