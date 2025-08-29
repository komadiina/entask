import { AsyncPipe, NgForOf } from '@angular/common';
import { NgIf } from '@angular/common';
import { ChangeDetectionStrategy, Component, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { ZardButtonComponent } from '@entask-components/button/button.component';
import { ZardDropdownModule } from '@entask-components/dropdown/dropdown.module';
import { HeaderComponent } from '@entask-components/header/header.component';
import { conversions as _conversions } from '@entask-constants/conversions/conversion-types.constant';
import { ConversionLabel } from '@entask-types/dashboard/conversion-label.type';
import {
	TFileConversionForm,
	TermExtractorForm,
	WaveformerForm,
} from '@entask-types/dashboard/forms.type';
import {
	WebSocketResponse,
	WebSocketResponseType,
	WebSocketWorkflowStatus,
} from '@entask-types/dashboard/websocket-response.type';
import { MessageService } from 'primeng/api';
import { Observable, map } from 'rxjs';
import { PresignRequest } from '@entask-models/file/presign-request.model';
import { AuthService } from '@entask-services/auth.service';
import { LocalStorageService } from '@entask-services/local-storage.service';
import { DashboardService } from '@entask-services/pages/dashboard.service';
import { GeneralWebSocket } from '@entask-services/websocket.class';

@Component({
	selector: 'app-dashboard',
	imports: [
		ZardDropdownModule,
		ZardButtonComponent,
		NgForOf,
		NgIf,
		HeaderComponent,
		AsyncPipe,
	],
	templateUrl: './dashboard.component.html',
	styleUrls: ['./dashboard.component.css'],
	changeDetection: ChangeDetectionStrategy.OnPush,
	standalone: true,
})
export class DashboardComponent implements OnDestroy {
	websocket: GeneralWebSocket<WebSocketResponse>;
	conversionStarted = false;
	serverResponse?: Observable<string>;
	conversionStatus: string;
	conversions: ConversionLabel[] = _conversions;
	selectedConversion: ConversionLabel | null = null;
	isConversionPaused = false;
	isConversionRunning = false;
	isAbortEnabled = true;
	isDownloadEnabled = false;

	textRecognizerForm: TFileConversionForm;
	thumbnailerForm: TFileConversionForm;
	waveformerForm: WaveformerForm;
	termExtractorForm: TermExtractorForm;
	conversionDownloadUri: string | null = null;

	constructor(
		private authService: AuthService,
		public router: Router,
		private messageService: MessageService,
		private dashboardService: DashboardService,
		private localStorageService: LocalStorageService,
	) {
		this.websocket = new GeneralWebSocket(null, true);

		this.serverResponse = this.websocket
			.getMessages()
			.pipe((data) => {
				data.subscribe((data) => {
					if (data.type === WebSocketResponseType.ProgressUpdate) {
						if (data?.status === WebSocketWorkflowStatus.Succeeded) {
							this.isConversionRunning = false;
							this.conversionStatus = 'Completed';
							this.conversionDownloadUri = data.data.downloadUri;

							this.isAbortEnabled = false;
							this.isDownloadEnabled = true;

							this.messageService.add({
								severity: 'success',
								summary: 'Conversion finished',
								detail: 'Conversion completed successfully!',
							});
						} else if (data?.status === WebSocketWorkflowStatus.Started) {
							this.localStorageService.set('workflowId', data.data.workflow_id);
							this.isConversionRunning = true;

							this.isAbortEnabled = true;
							this.isDownloadEnabled = false;

							this.messageService.add({
								severity: 'info',
								summary: 'Conversion started',
								detail:
									'Conversion has started: ' +
									(data.data.workflow_id ?? 'unknown_id'),
							});
						}
					}
				});

				return data;
			})
			.pipe(map((data) => data.message ?? 'Malformed response.'));

		this.conversionStatus = 'Pending...';

		this.textRecognizerForm = {
			contentType: 'image/jpeg',
			conversionType: 'text-recognizer',
		};

		this.thumbnailerForm = {
			contentType: 'video/mp4',
			conversionType: 'thumbnailer',
		};

		this.waveformerForm = {
			contentType: 'audio/wav',
			filters: {
				compress: false,
				reverb: false,
				gain: false,
				downmix: false,
			},
			conversionType: 'waveformer',
		};

		this.termExtractorForm = { contentType: 'text/plain' };
	}

	public logout(): void {
		this.authService.logout();
		this.router.navigate(['/login']);
	}

	public selectConversion(conversionType: ConversionLabel): void {
		this.selectedConversion = conversionType;
	}

	// --- text-recognizer --- //
	public submitRecognizer(): void {
		this.forwardUpload(this.textRecognizerForm);
	}

	public onResultNameChange(event: Event) {
		this.textRecognizerForm.resultName = (
			event.target as HTMLInputElement
		).value;
	}

	public onDescriptionChange(event: Event) {
		this.textRecognizerForm.description = (
			event.target as HTMLInputElement
		).value;
	}

	// --- waveformer --- //
	public submitWaveformer() {
		this.forwardUpload(this.waveformerForm);
	}

	public onWaveformerDescriptionChange($event: Event) {
		this.waveformerForm.description = ($event.target as HTMLInputElement).value;
	}

	public onWaveformerResultNameChange($event: Event) {
		this.waveformerForm.resultName = ($event.target as HTMLInputElement).value;
	}

	// --- thumbnailer --- //
	public submitThumbnailer() {
		this.forwardUpload(this.thumbnailerForm);
	}

	public onThumbnailerDescriptionChange($event: Event) {
		this.thumbnailerForm.description = (
			$event.target as HTMLInputElement
		).value;
	}

	public onThumbnailerResultNameChange($event: Event) {
		this.thumbnailerForm.resultName = ($event.target as HTMLInputElement).value;
	}

	// --- term-extractor --- //
	public submitTermExtractor() {
		throw new Error('submitTermExtractor not implemented.');
	}

	public onTermExtractorInput($event: Event) {
		this.termExtractorForm.content = ($event.target as HTMLInputElement).value;
	}

	public setFile<C extends TFileConversionForm>(
		target: C,
		event: Event,
		maxFileSizeB: number,
	) {
		const el = event.target as HTMLInputElement;
		if (el.files && el.files.length > 0) {
			if (el.files[0].size > maxFileSizeB) {
				this.messageService.add({
					severity: 'error',
					summary: 'File size error',
					detail: `File size must be less than ${this.toMB(maxFileSizeB)} megabytes.`,
				});
				return;
			}

			target.content = el.files[0];
		}
	}

	public toMB(fileSize: number) {
		return fileSize / 1024 / 1024;
	}

	public fromMB(amount: number) {
		return amount * 1024 * 1024;
	}

	private ensure(...args: any[]): boolean {
		let invalid = false;

		for (const arg of args) {
			if (!arg) {
				invalid = true;
			}
		}

		if (invalid) {
			this.messageService.add({
				severity: 'error',
				summary: 'Oops!',
				detail: 'Please fill in all required fields.',
				life: 4000,
			});
		}

		return invalid;
	}

	private async forwardUpload<T extends TFileConversionForm>(
		formBody: T,
	): Promise<void> {
		this.conversionStarted = true;

		this.messageService.add({
			severity: 'info',
			summary: 'Uploading',
			detail: 'Generating upload URL...',
		});

		const presignRequest: PresignRequest = {
			file: formBody.content! as File,
			filename: formBody.resultName!,
			conversionType: formBody.conversionType,
		};

		let resp = await this.dashboardService
			.getSignedUrl(presignRequest, presignRequest.file)
			.then((response) => {
				this.messageService.add({
					severity: 'success',
					summary: 'Success',
					detail: 'Upload URL generated successfully.',
				});
				return response;
			});

		resp = await this.dashboardService
			.uploadFile(resp, formBody)
			.then(async (response) => {
				this.messageService.add({
					severity: 'info',
					summary: 'Uploading',
					detail: 'Uploading file...',
				});

				await this.dashboardService.submitConversionRequest({
					...formBody,
					objectKey: resp.key,
					userId: resp.userId,
				});

				return response;
			});

		this.messageService.add({
			severity: 'success',
			summary: 'Success',
			detail: 'File uploaded successfully.',
		});
	}

	public downloadResult(): void {
		this.dashboardService.downloadResult(this.conversionDownloadUri!);
	}

	public cancelConversion(): void {
		this.dashboardService.cancelConversion().subscribe((data) => {
			if (data.success == true) {
				this.messageService.add({
					severity: 'success',
					summary: 'Success',
					detail: 'Conversion cancelled successfully.',
				});
			}
		});

		this.conversionStarted = false;
		this.conversionDownloadUri = null;
	}

	ngOnDestroy(): void {
		this.messageService.clear();
		this.websocket.close();
	}
}
