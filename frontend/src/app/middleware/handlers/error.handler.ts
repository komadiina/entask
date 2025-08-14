import { ErrorHandler } from '@angular/core';
import { MessageService } from 'primeng/api';

export class EntaskErrorHandler implements ErrorHandler {
	handleError(error: Error) {
		console.error(error);

		// show error message on primeng toast
		new MessageService().add({
			severity: 'error',
			summary: error.name,
			detail: error.message,
		});
	}
}

export const provideEntaskErrorHandler = () => ({
	provide: ErrorHandler,
	useClass: EntaskErrorHandler,
});
