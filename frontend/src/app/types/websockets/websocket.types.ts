export enum InterruptType {
	Abort = 'abort',
	Pause = 'pause',
	Resume = 'resume',
}

export interface WebSocketClientInterrupt {
	userId: string;
	workflowId: string;
	interruptType: InterruptType;
}

export enum ResponseType {
	ProgressUpdate = 'progress-update',
	Ack = 'ack',
	Error = 'error',
	Other = 'other',
}

export interface WebSocketResponse {
	type: ResponseType;
	clientId: string;
	status: string;
	message: string;
	data: any;
}
