import { AbstractControl, ValidationErrors } from '@angular/forms';

export const passwordsMatchValidator = (
	group: AbstractControl,
): ValidationErrors | null => {
	const password = group.get('password')?.value;
	const passwordConfirm = group.get('passwordConfirm')?.value;
	return password === passwordConfirm ? null : { passwordMismatch: true };
};

export const emailsMatchValidator = (
	group: AbstractControl,
): ValidationErrors | null => {
	const email = group.get('email')?.value;
	const emailConfirm = group.get('emailConfirm')?.value;
	return email === emailConfirm ? null : { emailMismatch: true };
};

export const passwordLengthValidator = (
	group: AbstractControl,
): ValidationErrors | null => {
	const password = group.get('password')?.value;
	return password && password.length >= 8 ? null : { passwordTooShort: true };
};
