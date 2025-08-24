import { NgForOf } from '@angular/common';
import { NgIf } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
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
import { MessageService } from 'primeng/api';
import { PresignRequest } from '@entask-models/file/presign-request.model';
import { AuthService } from '@entask-services/auth.service';
import { DashboardService } from '@entask-services/pages/dashboard.service';

@Component({
	selector: 'app-dashboard',
	imports: [
		ZardDropdownModule,
		ZardButtonComponent,
		NgForOf,
		NgIf,
		HeaderComponent,
	],
	templateUrl: './dashboard.component.html',
	styleUrls: ['./dashboard.component.css'],
	changeDetection: ChangeDetectionStrategy.OnPush,
	standalone: true,
})
export class DashboardComponent {
	conversions: ConversionLabel[] = _conversions;

	textRecognizerForm: TFileConversionForm = {
		contentType: 'image/jpeg',
		conversionType: 'text-recognizer',
	};

	thumbnailerForm: TFileConversionForm = {
		contentType: 'video/mp4',
		conversionType: 'thumbnailer',
	};

	waveformerForm: WaveformerForm = {
		contentType: 'audio/wav',
		filters: {
			compress: false,
			reverb: false,
			gain: false,
			downmix: false,
		},
		conversionType: 'waveformer',
	};

	termExtractorForm: TermExtractorForm = {
		contentType: 'text/plain',
	};

	selectedConversion: ConversionLabel | null = null;

	constructor(
		private authService: AuthService,
		public router: Router,
		private messageService: MessageService,
		private dashboardService: DashboardService,
	) {}

	public logout(): void {
		this.authService.logout();
		this.router.navigate(['/login']);
	}

	public selectConversion(conversionType: ConversionLabel): void {
		this.selectedConversion = conversionType;
	}

	// --- text-recognizer --- //
	public submitRecognizer(): void {
		this.textRecognizerForm.formData = new FormData();
		this.textRecognizerForm.formData.append(
			'file',
			this.textRecognizerForm.content!,
		);
		this.forwardUpload(this.textRecognizerForm);
		throw new Error('submitRecognizer not implemented.');
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
		throw new Error('submitWaveformer not implemented.');
	}

	public onWaveformerDescriptionChange($event: Event) {
		this.waveformerForm.description = ($event.target as HTMLInputElement).value;
	}

	public onWaveformerResultNameChange($event: Event) {
		this.waveformerForm.resultName = ($event.target as HTMLInputElement).value;
	}

	// --- thumbnailer --- //
	public submitThumbnailer() {
		// todo: add checks
		this.forwardUpload(this.thumbnailerForm);
		throw new Error('submitThumbnailer not implemented.');
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
				});

				return response;
			});

		this.messageService.add({
			severity: 'success',
			summary: 'Success',
			detail: 'File uploaded successfully.',
		});
	}
}
