import { Injectable } from '@angular/core';
import { KLocalStorage } from '@entask-types/local-storage/local-storage.type';
import { LocalStorageService } from '@entask-services/local-storage.service';
import { environment } from '@entask-environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiUtil {
	public static buildUrl(path: string, versioned = true): string {
		const apiVersion = LocalStorageService.get('apiVersion' as KLocalStorage);
		if (versioned && !apiVersion) {
			throw Error(
				`API version is not initialized - expected 'str', received ${apiVersion}.`,
			);
		}

		if (!path.startsWith('/')) path = `/${path}`;
		const url = `${environment.backendUrl}${versioned ? `/${apiVersion}` : ''}${path}`;
		return url;
	}
}
