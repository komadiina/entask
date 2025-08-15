import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ApiUtil } from '@entask-utilities/api/api.util';
import { Observable } from 'rxjs';
import { User } from '@entask-models/db/user.model';
import { RegistrationResponse } from '@entask-models/register/registration-response.model';

@Injectable({
	providedIn: 'root',
})
export class RegisterService {
	constructor(private http: HttpClient) {}

	public register(user: User): Observable<RegistrationResponse> {
		return this.http.post<RegistrationResponse>(
			ApiUtil.buildUrl('/auth/register'),
			user,
		);
	}
}
