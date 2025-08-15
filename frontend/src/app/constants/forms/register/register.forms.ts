import { FormBuilder, FormControl } from '@angular/forms';
import { Validators } from '@angular/forms';
import {
	emailsMatchValidator,
	passwordsMatchValidator,
} from '@entask-validators/register.validator';

export const registrationForm = (formBuilder: FormBuilder) =>
	formBuilder.group(
		{
			username: new FormControl('', [
				Validators.required,
				Validators.pattern(/^[a-zA-Z_]+$/),
				Validators.minLength(3),
				Validators.maxLength(24),
			]),
			password: new FormControl('', [
				Validators.required,
				Validators.minLength(8),
				Validators.maxLength(255),
			]),
			passwordConfirmed: new FormControl('', [
				Validators.required,
				Validators.minLength(8),
				Validators.maxLength(255),
			]),
			email: new FormControl('', [
				Validators.required,
				Validators.pattern(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/),
			]),
			emailConfirmed: new FormControl('', [
				Validators.required,
				Validators.pattern(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/),
			]),
			givenName: new FormControl('', [Validators.required]),
			familyName: new FormControl('', [Validators.required]),
		},
		{
			validators: [passwordsMatchValidator, emailsMatchValidator],
		},
	);
