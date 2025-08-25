import { WebSocketResponse } from '@entask-types/dashboard/websocket-response.type';
import { MessageService } from 'primeng/api';
import { Observable } from 'rxjs';
import { WebSocketSubject, webSocket } from 'rxjs/webSocket';
import { ApiUtil } from '@entask-utils/api/api.util';
import { wsObservers } from '@entask-utils/rxjs/observers/dashboard/websocket.observer';
import { environment } from '@entask-environments/environment';
import { LocalStorageService } from './local-storage.service';

export class GeneralWebSocket<TSent> {
	private socket: WebSocketSubject<any>;
	private _messageService: MessageService | null;

	public get messageService(): MessageService | null {
		return this._messageService;
	}

	constructor(
		url: string | null,
		useEnvironment: boolean,
		messageService: MessageService,
	) {
		if (useEnvironment) {
			const _url = ApiUtil.builder()
				.protocol('ws')
				.host(environment.backendHost)
				.port(environment.backendPort)
				.service('notifier')
				.endpoint(`/notify/client/${LocalStorageService.get('uuid')}`)
				.build();

			this.socket = webSocket(_url);
		} else {
			this.socket = webSocket(url!);
		}

		this._messageService = messageService;

		this.socket.subscribe(
			wsObservers.classicObserver.context(this as GeneralWebSocket<TSent>),
		);
	}

	public send(data: TSent): void {
		this.socket.next(JSON.stringify(data));
	}

	public getMessages(): Observable<WebSocketResponse> {
		return this.socket.asObservable();
	}

	public close(): void {
		this.socket.complete();
	}
}
