import { ChangeDetectionStrategy, Component } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { Ripple } from 'primeng/ripple';
import { Toast } from 'primeng/toast';
import { RedirectService } from '@entask-root/services/redirect.service';
import { AuthService } from '@entask-services/auth.service';

@Component({
	selector: 'app-login',
	imports: [Toast, Ripple, ButtonModule, ReactiveFormsModule],
	providers: [MessageService],
	templateUrl: './login.component.html',
	styleUrl: './login.component.css',
	changeDetection: ChangeDetectionStrategy.Default,
	standalone: true,
})
export class LoginComponent {
	usernameControl = new FormControl('');
	passwordControl = new FormControl('');

	constructor(
		private authService: AuthService,
		private messageService: MessageService,
		public redirectService: RedirectService,
	) {
		this.authService.hostComponent = this;

		if (authService.isLoggedIn()) {
			this.redirectService.redirect({ path: '/dashboard' }, true);
		}
	}

	public get getMessageService(): MessageService {
		return this.messageService;
	}

	public show(sev: string): void {
		this.messageService.add({
			severity: sev,
			summary: sev.toUpperCase(),
			detail: 'Lorem ipsum dolor sit amet consectetur adipiscing elit',
			life: 3500,
		});
	}

	public async login(): Promise<void> {
		if (
			this.usernameControl.value?.trim() == '' ||
			this.passwordControl.value?.trim() == ''
		) {
			this.messageService.add({
				severity: 'error',
				summary: 'Error',
				detail: 'Please enter valid login credentials.',
				life: 3500,
			});
			return;
		}

		this.authService.login(
			this.usernameControl.value!,
			this.passwordControl.value!,
		);
	}

	public async signup(): Promise<void> {
		this.redirectService.redirect({ path: '/register' }, false);
	}

	public async forgotPassword(): Promise<void> {
		this.redirectService.redirect({ path: '/forgotten-password' }, false);
	}

	public async signupGoogle(): Promise<void> {
		this.authService.signupGoogle();
	}

	public clearToast(): void {
		this.messageService.clear();
	}
}
