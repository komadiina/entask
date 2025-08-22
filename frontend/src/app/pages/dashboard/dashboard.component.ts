import { NgForOf } from '@angular/common';
import { NgIf } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ZardButtonComponent } from '@entask-root/components/button/button.component';
import { ZardDropdownModule } from '@entask-root/components/dropdown/dropdown.module';
import { HeaderComponent } from '@entask-root/components/header/header.component';
import { AuthService } from '@entask-services/auth.service';

interface ConversionLabel {
	name: string;
	value: string;
}

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
	conversions: any[] = [
		{
			name: 'Thumbnailer',
			value: 'thumbnailer',
		},
		{
			name: 'Text Recognizer',
			value: 'text-recognizer',
		},
		{
			name: 'Waveformer',
			value: 'waveformer',
		},
		{
			name: 'Term Extractor',
			value: 'term-extractor',
		},
	];

	recognizerForm: {
		file?: File;
		resultName?: string;
		description?: string | null;
	} = {};

	thumbnailerForm: {
		file?: File | null;
		resultName?: string;
		description?: string | null;
	} = {};

	waveformerForm: {
		file?: File;
		resultName?: string;
		description?: string | null;
		filters?: {
			compress: boolean;
			reverb: boolean;
			gain: boolean;
			downmix: boolean;
		};
	} = {
		filters: {
			compress: false,
			reverb: false,
			gain: false,
			downmix: false,
		},
	};

	termExtractorText = '';

	selectedConversion: ConversionLabel | null = null;

	constructor(
		private authService: AuthService,
		public router: Router,
		private messageService: MessageService,
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
		// TODO
		this.forwardUpload(this.recognizerForm, '');
		throw new Error('submitRecognizer not implemented.');
	}

	public onResultNameChange(event: Event) {
		this.recognizerForm.resultName = (event.target as HTMLInputElement).value;
	}

	public onDescriptionChange(event: Event) {
		this.recognizerForm.description = (event.target as HTMLInputElement).value;
	}

	// --- waveformer --- //
	public submitWaveformer() {
		this.ensure(
			this.waveformerForm.file,
			this.waveformerForm.description,
			this.waveformerForm.resultName,
		);
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
		this.termExtractorText = ($event.target as HTMLInputElement).value;
	}

	public setFile(target: any, event: Event, maxFileSizeB) {
		const el = event.target as HTMLInputElement;
		if (el.files && el.files.length > 0) {
			if (el.files[0].size > maxFileSizeB) {
				this.messageService.add({
					severity: 'error',
					summary: 'File size error',
					detail: `File size must be less than ${this.fromMB(maxFileSizeB)} megabytes.`,
				});
				return;
			}

			target.file = el.files[0];
		}
	}

	public fromMB(fileSize: number) {
		return fileSize / 1024 / 1024;
	}

	public toMB(amount: number) {
		return amount * 1024 * 1024;
	}

	private ensure(...args: any[]) {
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
	}

	private forwardUpload(formBody: any, presignedUrl: string): void {
		console.log(formBody, presignedUrl);
	}
}
