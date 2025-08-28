export enum WebSocketResponseType {
	ProgressUpdate = 'progress-update',
	Event = 'notification',
	Other = 'other',
}

export enum WebSocketWorkflowStatus {
	Running = 'running',
	Succeeded = 'succeeded',
	Failed = 'failed',
}

export interface WebSocketResponse {
	type: WebSocketResponseType;
	client_id: string;
	status: string;
	message: string;
	data: any;
}
