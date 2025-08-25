/**
 * Types of WebSocket messages (client-initiated, server-initiated).
 */
export enum WSMessageType {
	WorkflowInterrupt = 'workflow-interrupt',
	Notification = 'notification',
	Error = 'error',
	Other = 'other',
}

/**
 * Types of client-initiated workflow interrupts.
 */
export enum WFInterruptType {
	Abort = 'abort',
	Pause = 'pause',
	Resume = 'resume',
}

/**
 * Message acknowledgement status.
 */
export enum AckStatus {
	Ack = 'ack',
	Nack = 'nack',
}

export interface WebSocketClientInterrupt {
	/**
	 * Type of workflow interrupt (@see WFInterruptType).
	 * @see WFInterruptType
	 */
	signal: WFInterruptType;

	/**
	 * Conversion token used to identify the workflow engine worker node.
	 */
	token: string;
}

/**
 * WebSocket message sent to the websocket-facade server.
 */
export interface WebSocketClientMessage {
	/**
	 * Type of message (@see WSMessageType).
	 * @see WSMessageType
	 */
	type: WSMessageType;

	/**
	 * Message content.
	 * @see WebSocketClientInterrupt
	 */
	content: WebSocketClientInterrupt | any;
}

/**
 * WebSocket message sent to the websocket-facade server upon client-initiated workflow interrupts.
 */
export interface WebSocketInterruptResponse {
	/**
	 * Client message acknowledgement status.
	 */
	status: AckStatus;

	/**
	 * Error details, only if `status === AckStatus.Nack`.
	 */
	error: Error | undefined;
}

/**
 * WebSocket message received from the websocket-facade server.
 */
export interface WebSocketServerMessage {
	/**
	 * Server web-socket message content. If client initiates a workflow interrupt, contains result details.
	 * @see WebSocketInterruptResponse
	 */
	data: WebSocketInterruptResponse | any;
}
