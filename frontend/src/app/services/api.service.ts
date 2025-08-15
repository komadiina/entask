import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { TLocalStorage } from '@entask-types/local-storage/local-storage.type';
import { Observable, lastValueFrom } from 'rxjs';
import { LocalStorageService } from '@entask-services/local-storage.service';
import { ApiUtil } from '@entask-utils/api/api.util';

@Injectable({
	providedIn: 'root',
})
export class APIService {
	constructor(
		private http: HttpClient,
		private localStorageService: LocalStorageService,
	) {}

	public getApiVersion(): Observable<{ version: string }> {
		return this.http.get<{ version: string }>(
			ApiUtil.buildUrl('/version', false),
		);
	}

	public async initApi(): Promise<void> {
		const response = await lastValueFrom(this.getApiVersion());
		this.localStorageService.set(
			'apiVersion',
			response.version as TLocalStorage['apiVersion'],
		);
	}
}
