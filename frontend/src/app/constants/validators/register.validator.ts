import { AbstractControl, ValidationErrors } from '@angular/forms';

export const passwordsMatchValidator = (
	group: AbstractControl,
): ValidationErrors | null => {
	const password = group.get('password')?.value;
	const passwordConfirmed = group.get('passwordConfirmed')?.value;
	return password === passwordConfirmed ? null : { passwordMismatch: true };
};

export const emailsMatchValidator = (
	group: AbstractControl,
): ValidationErrors | null => {
	const email = group.get('email')?.value;
	const emailConfirmed = group.get('emailConfirmed')?.value;
	return email === emailConfirmed ? null : { emailMismatch: true };
};

export const passwordLengthValidator = (
	group: AbstractControl,
): ValidationErrors | null => {
	const password = group.get('password')?.value;
	return password && password.length >= 8 ? null : { passwordTooShort: true };
};
