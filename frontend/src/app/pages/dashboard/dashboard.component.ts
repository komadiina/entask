import { ChangeDetectionStrategy, Component } from '@angular/core';
import { AuthService } from '@entask-services/auth.service';

@Component({
	selector: 'app-dashboard',
	imports: [],
	templateUrl: './dashboard.component.html',
	styleUrl: './dashboard.component.css',
	changeDetection: ChangeDetectionStrategy.OnPush,
	standalone: true,
})
export class DashboardComponent {
	constructor(private authService: AuthService) {}
}
