import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Toast } from 'primeng/toast';
import { APIService } from '@entask-services/api.service';
import { LocalStorageService } from '@entask-services/local-storage.service';

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

	constructor(
		private apiClient: APIService,
		private localStorageService: LocalStorageService,
	) {
		this.apiClient.initApi();
	}
}
