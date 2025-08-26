import { Observable, map } from 'rxjs';
import { WebSocketSubject, webSocket } from 'rxjs/webSocket';
import { ApiUtil } from '@entask-utils/api/api.util';
import { environment } from '@entask-environments/environment';
import { LocalStorageService } from './local-storage.service';

export class GeneralWebSocket<TSent> {
	private socket: WebSocketSubject<any>;

	constructor(url: string | null, useEnvironment: boolean) {
		if (useEnvironment) {
			const _url = ApiUtil.builder()
				.protocol('ws')
				.host(environment.backendHost)
				.port(environment.backendPort)
				.noRootPrefix()
				.service('ws')
				.endpoint(`/${LocalStorageService.get('uuid')}`)
				.build();

			this.socket = webSocket(_url);
		} else {
			this.socket = webSocket(url!);
		}
	}

	public send(data: TSent): void {
		this.socket.next(JSON.stringify(data));
	}

	public getMessages(): Observable<any> {
		return this.socket.asObservable().pipe(map((data) => JSON.parse(data)));
	}

	public close(): void {
		this.socket.complete();
	}
}
