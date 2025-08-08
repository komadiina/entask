import { Component, inject } from '@angular/core';
import {
	AbstractControl,
	FormBuilder,
	FormGroup,
	ReactiveFormsModule,
	ValidationErrors,
} from '@angular/forms';
import { registrationForm } from '@entask-constants/forms/registration.constants';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { Ripple } from 'primeng/ripple';
import { Toast } from 'primeng/toast';
import { RegistrationPartial } from '@entask-root/types/registration/registration_form.type';

@Component({
	selector: 'app-register',
	imports: [ButtonModule, Ripple, ReactiveFormsModule, Toast],
	templateUrl: './register.component.html',
	styleUrl: './register.component.css',
})
export class RegisterComponent {
	private formBuilder = inject(FormBuilder);
	registrationForm: FormGroup;

	constructor(private messageService: MessageService) {
		this.registrationForm = this.initForm(this.formBuilder);
	}

	public submitRegister(): void {
		let invalidRequest = false;

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
			this.messageService.add({
				severity: 'success',
				summary: 'Success',
				detail: 'Registration requested successfully.',
				life: 4000,
			});
		}
	}

	private highlightFields(fields: string[]): void {
		fields.forEach((field) => {
			this.registrationForm.get(field)?.setErrors({ invalid: true });
			document.getElementById(field)?.classList.add('p-invalid');
		});
	}

	private removeHighlights(fields: string[]): void {
		fields.forEach((field) => {
			this.registrationForm.get(field)?.setErrors(null);
			document.getElementById(field)?.classList.remove('p-invalid');
		});
	}

	private initForm(builder: FormBuilder): FormGroup {
		let form: FormGroup = registrationForm(builder);

		form = this.initCustomValidators(form);

		form.valueChanges.subscribe((value: RegistrationPartial) => {
			console.log(value);

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

	private initCustomValidators(formGroup: FormGroup): FormGroup {
		// -- Check for password/passwordConfirm mismatch
		formGroup.get('passwordConfirm')?.addValidators([
			(control: AbstractControl): ValidationErrors | null => {
				if (control.value !== formGroup.get('password')?.value) {
					formGroup.setErrors({ invalid: true, passwordMismatch: true });
					return { invalid: true, passwordMismatch: true };
				}

				return null;
			},
		]);

		// -- Check for email/emailConfirm mismatch
		formGroup.get('emailConfirm')?.addValidators([
			(control: AbstractControl): ValidationErrors | null => {
				if (control.value !== formGroup.get('email')?.value) {
					formGroup.setErrors({ invalid: true, emailMismatch: true });
					return { invalid: true, emailMismatch: true };
				}

				return null;
			},
		]);

		return formGroup;
	}
}
