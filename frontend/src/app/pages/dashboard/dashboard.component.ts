import {
	ChangeDetectionStrategy,
	Component,
	OnChanges,
	OnInit,
	SimpleChanges,
} from '@angular/core';
import { AuthService } from '@entask-services/auth.service';

@Component({
	selector: 'app-dashboard',
	imports: [],
	templateUrl: './dashboard.component.html',
	styleUrl: './dashboard.component.css',
	changeDetection: ChangeDetectionStrategy.OnPush,
	standalone: true,
})
export class DashboardComponent implements OnInit, OnChanges {
	constructor(private authService: AuthService) {}

	ngOnInit(): void {
	}

	ngOnChanges(changes: SimpleChanges): void {
	}
}
