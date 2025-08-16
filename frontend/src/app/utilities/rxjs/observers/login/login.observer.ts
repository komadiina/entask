import { BaseObserver } from '@entask-utilities/rxjs/observers/base.observer';
import { LoginResponse } from '@entask-models/login/login-response.model';
import { LocalStorageService } from '@entask-services/local-storage.service';

export const loginObservers = {
	loginSubmit: new BaseObserver<LoginResponse, null>(
		(value: LoginResponse): void => {
			LocalStorageService.set('accessToken', value.accessToken);
			LocalStorageService.set('refreshToken', value.refreshToken);
			LocalStorageService.set('idToken', value.idToken);
		},

		(error: Error): void => {
			console.error(error);
		},

		(): void => {
			console.log('complete');
		},
	),
};
