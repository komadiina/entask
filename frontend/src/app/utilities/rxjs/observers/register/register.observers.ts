import { BaseObserver } from '@entask-utilities/rxjs/observers/base.observer';
import { RegisterComponent } from '@entask-pages/register/register.component';
import { RegistrationResponse } from '@entask-models/register/registration-response.model';

export const registerObservers = {
	registrationSubmit: new BaseObserver<RegistrationResponse, RegisterComponent>(
		(value: RegistrationResponse, ctx?: RegisterComponent | null) => {
			console.log(value);
			ctx?.registrationForm.reset();
		},

		(error: Error, ctx?: RegisterComponent | null) => {
			ctx?.getMessageService.add({
				severity: 'error',
				summary: 'Error',
				detail: 'Registration failed. Check console for more details.',
			});
		},

		(ctx?: RegisterComponent | null) => {
			ctx?.getMessageService.add({
				severity: 'success',
				summary: 'Success',
				detail: 'Registration successful.',
			});
		},
	),
};
