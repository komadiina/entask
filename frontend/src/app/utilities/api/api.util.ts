import { Injectable } from '@angular/core';
import { environment } from '@entask-environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiUtil {
	public static buildUrl(path: string): string {
		if (!path.startsWith('/')) path = `/${path}`;
		const url = `${environment.backendHost}${path}`;
		return url;
	}

	public static builder(): ApiEndpointBuilder {
		return new ApiEndpointBuilder();
	}
}

class ApiEndpointBuilder {
	private _protocol: string;
	private _host: string;
	private _port: string;
	private _rootPrefix: string;
	private _prefix: string;
	private _endpoint: string;
	private _queryParams: Record<string, string> | null = null;

	constructor() {
		this._protocol = environment.backendProtocol;
		this._host = environment.backendHost;
		this._port = environment.backendPort;
		this._rootPrefix = '/' + environment.backendRootPrefix;

		this._prefix = this._endpoint = '';
	}

	/**
	 *
	 * @param protocol Network transfer protocol (e.g. `http`, `https`, `ws`, `ftp`, etc.)
	 * @returns {ApiEndpointBuilder} The current builder instance
	 */
	public protocol(protocol: string): ApiEndpointBuilder {
		this._protocol = protocol;
		return this;
	}

	public queryParam(key: string, value: string): ApiEndpointBuilder {
		if (!this._queryParams) this._queryParams = {};

		this._queryParams[key] = value;
		return this;
	}

	public queryParams(queryParams: Record<string, string>): ApiEndpointBuilder {
		this._queryParams = { ...this._queryParams, ...queryParams };
		return this;
	}

	/**
	 *
	 * @param host The host (e.g. `localhost`, '127.0.0.1`)
	 * @returns {ApiEndpointBuilder} The current builder instance
	 */
	public host(host: string): ApiEndpointBuilder {
		this._host = host;
		return this;
	}

	/**
	 *
	 * @param port Port that the service listens on (e.g. `80`, `4201`)
	 * @returns {ApiEndpointBuilder} The current builder instance
	 */
	public port(port: string): ApiEndpointBuilder {
		this._port = port;
		return this;
	}

	/**
	 * Removes the root prefix (e.g. `'/api'` from `'/api/auth/login'`)
	 * @returns {ApiEndpointBuilder} The current builder instance
	 */
	public noRootPrefix(): ApiEndpointBuilder {
		this._rootPrefix = '';
		return this;
	}

	/**
	 *
	 * @param prefix The custom prefix of the endpoint (e.g. `/private_api`). Do not use this to set the service name.
	 * @returns {ApiEndpointBuilder} The current builder instance
	 */
	public prefix(prefix: string): ApiEndpointBuilder {
		if (!prefix.startsWith('/')) prefix = `/${prefix}`;
		this._prefix = prefix;
		return this;
	}

	/**
	 *
	 * @param serviceName The name of the root service endpoint (e.g. `auth`, `conversion`, etc.)
	 * @returns {ApiEndpointBuilder} The current builder instance
	 */
	public service = (serviceName: string): ApiEndpointBuilder =>
		this.prefix(serviceName);

	/**
	 *
	 * @param bc The breadcrumb of the endpoint (e.g. `login` in `/login/auth`).
	 * @returns {ApiEndpointBuilder} The current builder instance
	 */
	public breadcrumb(bc: string): ApiEndpointBuilder {
		if (bc.startsWith('/')) bc = bc.slice(1);
		this._endpoint = `${this._endpoint}/${bc}`;
		return this;
	}

	/**
	 *
	 * @param bcs An array of endpoint breadcrumbs (e.g. `['client', 'notify'] for `/client/notify`). Used to initialize the `endpoint` property.
	 * @returns {ApiEndpointBuilder} The current builder instance
	 */
	public breadcrumbs(...bcs: string[]): ApiEndpointBuilder {
		bcs.forEach((bc) => this.breadcrumb(bc));
		return this;
	}

	/**
	 *
	 * @param endpoint The endpoint as a fixed variable (e.g. `/auth/login`)
	 * @returns {ApiEndpointBuilder} The current builder instance
	 */
	public endpoint(endpoint: string): ApiEndpointBuilder {
		if (!endpoint.startsWith('/')) endpoint = `/${endpoint}`;
		this._endpoint = endpoint;
		return this;
	}

	/**
	 *
	 * @returns {string} The built endpoint using previously set parameters (`protocol`, `host`, `port`, `(prefix | service)`, `(breadcrumb | breadcrumbs | endpoint`)
	 */
	public build(): string {
		const url = `${this._protocol}://${this._host}:${this._port}${this._rootPrefix}${this._prefix}${this._endpoint}`;

		if (this._queryParams) {
			return `${url}?${Object.entries(this._queryParams)
				.map(([key, value]) => `${key}=${value}`)
				.join('&')}`;
		}
		return url;
	}
}
