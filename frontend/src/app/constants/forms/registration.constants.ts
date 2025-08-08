import { FormBuilder, FormControl } from '@angular/forms';
import { Validators } from '@angular/forms';
import { emailValidator } from '@entask-utilities/auth/validators.util';

export const registrationForm = (formBuilder: FormBuilder) =>
	formBuilder.group({
		username: new FormControl('', [
			Validators.required,
			Validators.pattern(/^[a-zA-Z_]+$/),
			Validators.min(3),
			Validators.max(24),
		]),
		password: new FormControl('', [
			Validators.required,
			Validators.min(8),
			Validators.max(255),
		]),
		passwordConfirm: new FormControl('', [
			Validators.required,
			Validators.min(8),
			Validators.max(255),
		]),
		email: new FormControl('', [Validators.required, emailValidator]),
		emailConfirm: new FormControl('', [Validators.required, emailValidator]),
		givenName: new FormControl('', [Validators.required]),
		lastName: new FormControl('', [Validators.required]),
	});
