import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Toast } from 'primeng/toast';
import { APIService } from './services/api.service';

@Component({
	selector: 'app-root',
	imports: [RouterOutlet, Toast],
	templateUrl: './app.component.html',
	styleUrl: './app.component.css',
	standalone: true,
})
export class AppComponent {
	isCollapsed = false;
	history: History = window.history;

	constructor(private apiClient: APIService) {
		this.apiClient.getApiVersion().subscribe((res) => {
			localStorage.setItem('apiVersion', res.version);
		});
	}
}
