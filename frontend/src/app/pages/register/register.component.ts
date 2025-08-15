import { Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { Ripple } from 'primeng/ripple';
import { registrationForm } from '@entask-root/constants/forms/register/register.forms';
import { RegisterService } from '@entask-root/services/pages/register.service';
import { registerObservers } from '@entask-root/utilities/rxjs/observers/register/register.observers';

@Component({
	selector: 'app-register',
	imports: [ButtonModule, Ripple, ReactiveFormsModule],
	templateUrl: './register.component.html',
	styleUrl: './register.component.css',
	standalone: true,
})
export class RegisterComponent {
	public registrationForm: FormGroup;
	private formBuilder = inject(FormBuilder);

	constructor(
		private messageService: MessageService,
		private registerService: RegisterService,
	) {
		this.registrationForm = this.initForm(this.formBuilder);
	}

	get getMessageService(): MessageService {
		return this.messageService;
	}

	public submitRegister(): void {
		let invalidRequest = false;

		if (this.registrationForm.invalid) {
			console.log(this.registrationForm);
			invalidRequest = true;
			this.highlightEmptyFields();
			this.messageService.add({
				severity: 'error',
				summary: 'Oops!',
				detail: 'Please fill in all required fields.',
				life: 4000,
			});
		}

		if (this.registrationForm.hasError('passwordMismatch')) {
			invalidRequest = true;
			this.highlightFields(['password', 'passwordConfirmed']);
			this.messageService.add({
				severity: 'error',
				summary: 'Oops!',
				detail: 'Passwords do not match.',
				life: 4000,
			});
		}

		if (this.registrationForm.hasError('emailMismatch')) {
			invalidRequest = true;
			this.highlightFields(['email', 'emailConfirmed']);
			this.messageService.add({
				severity: 'error',
				summary: 'Oops!',
				detail: 'Email addresses do not match.',
				life: 4000,
			});
		}

		if (!invalidRequest) {
			this.removeAllHighlights();
			this.messageService.add({
				severity: 'info',
				summary: 'Registration',
				detail:
					'Registration requested successfully. You may now go back to log-in.',
				life: 5000,
			});

			this.registerService
				.register(this.registrationForm.value)
				.subscribe(registerObservers.registrationSubmit.context(this));
		}
	}

	private highlightEmptyFields(): void {
		const form: HTMLElement = document.getElementById('registrationForm')!;
		form.querySelectorAll('input').forEach((input) => {
			if (input.getAttribute('required') != null && input.value.trim() === '') {
				input.classList.add('p-invalid');
			}
		});
	}

	private removeAllHighlights(): void {
		this.removeHighlights([
			'email',
			'emailConfirmed',
			'password',
			'passwordConfirmed',
			'givenName',
			'familyName',
			'username',
		]);
	}

	private highlightFields(fields: string[]): void {
		fields.forEach((field) => {
			document.getElementById(field)?.classList.add('p-invalid');
		});
	}

	private removeHighlights(fields: string[]): void {
		fields.forEach((field) => {
			document.getElementById(field)?.classList.remove('p-invalid');
		});
	}

	private initForm(builder: FormBuilder): FormGroup {
		const form: FormGroup = registrationForm(builder);

		form.statusChanges.subscribe(() => {
			if (form.hasError('passwordMismatch')) {
				this.highlightFields(['password', 'passwordConfirmed']);
			} else {
				this.removeHighlights(['password', 'passwordConfirmed']);
			}

			if (form.hasError('emailMismatch')) {
				this.highlightFields(['email', 'emailConfirmed']);
			} else {
				this.removeHighlights(['email', 'emailConfirmed']);
			}
		});

		return form;
	}
}
