import { Validators } from '@angular/forms';

export function passwordValidator() {
	return Validators.pattern(
		/^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/,
	);
}

export function emailValidator() {
	return Validators.pattern(/^[a-zA-Z0-9.-]+@([a-zA-Z0-9-]+\.[a-zA-Z])+$/);
}

export function usernameValidator() {
	return Validators.pattern(
		/^(?=[a-zA-Z0-9._]{3,20}$)(?!.*[_.]{2})[^_.].*[^_.]$/,
	);
}
