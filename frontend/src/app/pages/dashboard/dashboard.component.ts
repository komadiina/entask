import { NgForOf } from '@angular/common';
import { NgIf } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { Router } from '@angular/router';
import { ZardButtonComponent } from '@entask-root/components/button/button.component';
import { ZardDropdownModule } from '@entask-root/components/dropdown/dropdown.module';
import { AuthService } from '@entask-services/auth.service';

@Component({
	selector: 'app-dashboard',
	imports: [ZardDropdownModule, ZardButtonComponent, NgForOf, NgIf],
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

	selectedConversion: string | null = null;

	constructor(
		private authService: AuthService,
		public router: Router,
	) {}

	public logout(): void {
		this.authService.logout();
		this.router.navigate(['/login']);
	}

	public selectConversion(conversionType: string): void {
		this.selectedConversion = conversionType;
	}

	submitRecognizer(): void {
		console.log('TODO: submitRecognizer');
	}

	onFileSelected(event) {
		this.recognizerForm.file = event.target?.files[0] ?? null;
		console.log(event);
	}

	onResultNameChange(event) {
		console.log(event);
	}

	onDescriptionChange(event) {
		console.log(event);
	}
}
