import { Injectable } from '@angular/core';
import { environment } from '@entask-environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiUtil {
	public static buildUrl(path: string): string {
		if (!path.startsWith('/')) path = `/${path}`;
		const url = `${environment.backendUrl}${path}`;
		return url;
	}
}
