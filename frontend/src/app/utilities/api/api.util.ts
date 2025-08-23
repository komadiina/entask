import { Injectable } from '@angular/core';
import { environment } from '@entask-environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiUtil {
	public static buildUrl(path: string): string {
		if (!path.startsWith('/')) path = `/${path}`;
		const url = `${environment.backendUrl}${path}`;
		return url;
	}

	public static builder(): ApiEndpointBuilder {
		return new ApiEndpointBuilder();
	}
}

class ApiEndpointBuilder {
	private _url: string;

	private _prefix: string;
	private _endpoint: string;

	constructor() {
		this._prefix = this._endpoint = '';
		this._url = environment.backendUrl;

		if (this._url.endsWith('/')) this._url = this._url.slice(0, -1);
	}

	public prefix(prefix: string): ApiEndpointBuilder {
		this._prefix = prefix;
		return this;
	}

	public service = (serviceName: string): ApiEndpointBuilder =>
		this.prefix(serviceName);

	public breadcrumb(bc: string): ApiEndpointBuilder {
		if (bc.startsWith('/')) bc = bc.slice(1);
		this._endpoint = `${this._endpoint}/${bc}`;
		return this;
	}

	public breadcrumbs(...bcs: string[]): ApiEndpointBuilder {
		bcs.forEach((bc) => this.breadcrumb(bc));
		return this;
	}

	public endpoint(endpoint: string): ApiEndpointBuilder {
		if (!endpoint.startsWith('/')) endpoint = `/${endpoint}`;
		this._endpoint = endpoint;
		return this;
	}

	public build(): string {
		return `${this._url}/${this._prefix}${this._endpoint}`;
	}
}
