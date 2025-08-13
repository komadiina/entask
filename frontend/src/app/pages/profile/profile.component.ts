import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
	selector: 'app-profile',
	imports: [],
	templateUrl: './profile.component.html',
	styleUrl: './profile.component.css',
	changeDetection: ChangeDetectionStrategy.OnPush,
	standalone: true,
})
export class ProfileComponent {}
