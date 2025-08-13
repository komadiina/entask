import { Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { Ripple } from 'primeng/ripple';
import { registrationForm } from '@entask-root/constants/forms/register/register.forms';

@Component({
	selector: 'app-register',
	imports: [ButtonModule, Ripple, ReactiveFormsModule],
	templateUrl: './register.component.html',
	styleUrl: './register.component.css',
	standalone: true,
})
export class RegisterComponent {
	private formBuilder = inject(FormBuilder);
	registrationForm: FormGroup;

	constructor(private messageService: MessageService) {
		this.registrationForm = this.initForm(this.formBuilder);
	}

	public submitRegister(): void {
		let invalidRequest = false;

		if (this.registrationForm.invalid) {
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
			this.highlightFields(['password', 'passwordConfirm']);
			this.messageService.add({
				severity: 'error',
				summary: 'Oops!',
				detail: 'Passwords do not match.',
				life: 4000,
			});
		}

		if (this.registrationForm.hasError('emailMismatch')) {
			invalidRequest = true;
			this.highlightFields(['email', 'emailConfirm']);
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
				severity: 'success',
				summary: 'Success',
				detail: 'Registration requested successfully.',
				life: 4000,
			});
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
			'emailConfirm',
			'password',
			'passwordConfirm',
			'givenName',
			'lastName',
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
				console.log('passwordMismatch');
				this.highlightFields(['password', 'passwordConfirm']);
			} else {
				this.removeHighlights(['password', 'passwordConfirm']);
			}

			if (form.hasError('emailMismatch')) {
				console.log('emailMismatch');
				this.highlightFields(['email', 'emailConfirm']);
			} else {
				this.removeHighlights(['email', 'emailConfirm']);
			}
		});

		return form;
	}
}
