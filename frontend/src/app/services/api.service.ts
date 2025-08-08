import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { apiConfig } from '@entask-constants/api.constants';
import { Observable } from 'rxjs';

@Injectable({
	providedIn: 'root',
})
export class APIService {
	constructor(private http: HttpClient) {}

	public getApiVersion(): Observable<{ version: string }> {
		return this.http.get<{ version: string }>(apiConfig.baseUrl + '/version');
	}
}
