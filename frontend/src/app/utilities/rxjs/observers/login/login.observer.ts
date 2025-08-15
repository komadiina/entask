import { BaseObserver } from '@entask-utilities/rxjs/observers/base.observer';
import { LoginResponse } from '@entask-models/login/login-response.model';

export const loginObservers = {
	loginSubmit: new BaseObserver<LoginResponse, null>(
		(value: LoginResponse): void => {
			console.log(value);
		},

		(error: Error): void => {
			console.error(error);
		},

		(): void => {
			console.log('complete');
		},
	),
};
