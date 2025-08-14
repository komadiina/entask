import { Injectable } from '@angular/core';
import { TLocalStorage } from '@entask-types/local-storage/local-storage.type';
import { LocalStorageService } from '@entask-services/local-storage.service';
import { environment } from '@entask-environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiUtil {
	public static buildUrl(path: string): string {
		if (LocalStorageService.get('apiVersion' as keyof TLocalStorage) === null) {
			throw Error(
				"API version is not initialized - expected 'str', received null.",
			);
		}

		if (!path.startsWith('/')) path = `/${path}`;

		return `${environment.backendUrl}/${LocalStorageService.get('apiVersion' as keyof TLocalStorage)}${path}`;
	}
}
