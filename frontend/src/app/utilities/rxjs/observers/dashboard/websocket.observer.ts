import { WebSocketResponse } from '@entask-types/dashboard/websocket-response.type';
import { GeneralWebSocket } from '@entask-services/websocket.class';
import { BaseObserver } from '../base.observer';

export const wsObservers = {
	classicObserver: new BaseObserver<WebSocketResponse, GeneralWebSocket<any>>(
		(value: WebSocketResponse, ctx?: GeneralWebSocket<any> | null) => {
			if (ctx && ctx.messageService) {
				ctx.messageService.add({
					severity: 'info',
					summary: 'WebSockets',
					detail: 'Message received from server: ' + value.status,
				});
			}
		},

		(error: Error, ctx?: any | null) => {
			console.error(error);

			if (ctx && ctx.messageService) {
				ctx.messageService.add({
					severity: 'error',
					summary: 'Error',
					detail: 'Error: ' + error.message,
				});
			}
		},

		(ctx?: any | null) => {
			// noop
		},
	),
};
