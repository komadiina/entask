import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';

export const globalHttpErrorInterceptor: HttpInterceptorFn = (req, next) =>
	next(req).pipe(
		catchError((error: HttpErrorResponse) => {
			console.error(error);
			return throwError(() => error);
		}),
	);
