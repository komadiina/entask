import { HttpEvent, HttpHandlerFn, HttpRequest } from '@angular/common/http';
import { KLocalStorage } from '@entask-types/local-storage/local-storage.type';
import { Observable } from 'rxjs';
import { LocalStorageService } from '@entask-services/local-storage.service';

export function authInterceptor(
	req: HttpRequest<unknown>,
	next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> {
	// append opaque access token (for authorization)
	const accessToken = LocalStorageService.get('accessToken' as KLocalStorage);
	if (accessToken) req.headers.append('Authorization', `Bearer ${accessToken}`);

	// append id token (for authorization)
	const idToken = LocalStorageService.get('idToken' as KLocalStorage);
	if (idToken) req.headers.append('x-id-token', `${idToken}`);

	const refreshToken = LocalStorageService.get('refreshToken' as KLocalStorage);
	if (refreshToken) req.headers.append('x-refresh-token', `${refreshToken}`);

	const authProvider = LocalStorageService.get('authProvider' as KLocalStorage);
	if (authProvider) req.headers.append('x-auth-type ', `${authProvider}`);

	return next(req);
}
