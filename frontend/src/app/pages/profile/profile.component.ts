import { ChangeDetectionStrategy, Component } from '@angular/core';
import { AuthService } from '@entask-services/auth.service';

@Component({
	selector: 'app-profile',
	imports: [],
	templateUrl: './profile.component.html',
	styleUrl: './profile.component.css',
	changeDetection: ChangeDetectionStrategy.Default,
})
export class ProfileComponent {
	constructor(private authService: AuthService) {}
}
