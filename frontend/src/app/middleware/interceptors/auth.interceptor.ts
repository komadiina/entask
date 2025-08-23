import {
	HttpEvent,
	HttpHandlerFn,
	HttpHeaders,
	HttpRequest,
} from '@angular/common/http';
import { KLocalStorage } from '@entask-types/local-storage/local-storage.type';
import { Observable } from 'rxjs';
import { LocalStorageService } from '@entask-services/local-storage.service';

export function authInterceptor(
	req: HttpRequest<unknown>,
	next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
	const accessToken = LocalStorageService.get('accessToken' as KLocalStorage);
	const idToken = LocalStorageService.get('idToken' as KLocalStorage);
	const refreshToken = LocalStorageService.get('refreshToken' as KLocalStorage);
	const authProvider = LocalStorageService.get('authProvider' as KLocalStorage);

	let headers: HttpHeaders = new HttpHeaders();
	headers = headers.set('Authorization', `Bearer ${accessToken}`);
	headers = headers.set('x-id-token', `${idToken}`);
	headers = headers.set('x-refresh-token', `${refreshToken}`);
	headers = headers.set('x-auth-type', `${authProvider}`);

	console.log(req.url, req.headers.getAll('Content-Length'));

	req = req.clone({
		headers: headers,
	});

	return next(req);
}
