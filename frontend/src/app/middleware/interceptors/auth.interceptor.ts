import { HttpEvent, HttpHandlerFn, HttpRequest } from '@angular/common/http';
import { TLocalStorage } from '@entask-types/local-storage/local-storage.type';
import { Observable } from 'rxjs';
import { LocalStorageService } from '@entask-services/local-storage.service';

export function authInterceptor(
	req: HttpRequest<unknown>,
	next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
	req.headers.append(
		'Authorization',
		'Bearer ' + LocalStorageService.get('accessToken' as keyof TLocalStorage),
	);
	return next(req);
}
