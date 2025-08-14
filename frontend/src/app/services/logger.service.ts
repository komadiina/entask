import { Injectable } from '@angular/core';
import { AppComponent } from '@entask-root/app.component';
import { LogLevel } from '@entask-constants/logger.constants';

@Injectable({
	providedIn: 'root',
})
export class LoggerService {
	private logLevel: string = LogLevel.DEBUG;
	private logPrefix: string = AppComponent.name;

	set LogLevel(value: string) {
		this.logLevel = value;
	}

	set LogPrefix(value: string) {
		this.logPrefix = value;
	}

	public init(metadata: { logLevel: LogLevel; logPrefix: string }): void {
		this.logLevel = metadata.logLevel;
		this.logPrefix = metadata.logPrefix;
	}

	public log(message: string[]): void {
		if (this.logLevel == LogLevel.PRODUCTION) {
			return;
		}

		if (this.logLevel == LogLevel.DEBUG) {
			console.log(`${this.logPrefix}: ${message}`);
		} else if (this.logLevel == LogLevel.INFO) {
			console.info(`${this.logPrefix}: ${message}`);
		} else if (this.logLevel == LogLevel.WARN) {
			console.warn(`${this.logPrefix}: ${message}`);
		} else if (this.logLevel == LogLevel.ERROR) {
			console.error(`${this.logPrefix}: ${message}`);
		}
	}
}
