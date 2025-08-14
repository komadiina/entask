import { FormBuilder, FormControl } from '@angular/forms';
import { Validators } from '@angular/forms';
import {
	emailsMatchValidator,
	passwordsMatchValidator,
} from '@entask-validators/register.validator';

export const registrationForm = (formBuilder: FormBuilder) =>
	formBuilder.group(
		{
			username: new FormControl(null, [
				Validators.required,
				Validators.pattern(/^[a-zA-Z ]+$/),
				Validators.min(3),
				Validators.max(24),
			]),
			password: new FormControl(null, [
				Validators.required,
				Validators.min(8),
				Validators.max(255),
			]),
			passwordConfirmed: new FormControl(null, [
				Validators.required,
				Validators.min(8),
				Validators.max(255),
			]),
			email: new FormControl(null, [
				Validators.required,
				Validators.pattern(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/),
			]),
			emailConfirmed: new FormControl(null, [
				Validators.required,
				Validators.pattern(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/),
			]),
			givenName: new FormControl(null, [Validators.required]),
			familyName: new FormControl(null, [Validators.required]),
		},
		{
			validators: [passwordsMatchValidator, emailsMatchValidator],
		},
	);
