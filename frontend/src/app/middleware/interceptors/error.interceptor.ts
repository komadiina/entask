import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { MessageService } from 'primeng/api';
import { catchError, throwError } from 'rxjs';

export const globalHttpErrorInterceptor: HttpInterceptorFn = (req, next) => {
	const messageService = inject(MessageService);

	return next(req).pipe(
		catchError((error: HttpErrorResponse) => {
			messageService.add({
				severity: 'error',
				summary: 'HTTP Error',
				detail: error.error?.detail ?? error.message,
			});
			return throwError(() => error);
		}),
	);
};
