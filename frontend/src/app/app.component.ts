import { NgIf } from '@angular/common';
import { Component } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { Toast } from 'primeng/toast';
import { APIService } from '@entask-services/api.service';
import { LocalStorageService } from '@entask-services/local-storage.service';
import { ZardButtonComponent } from './components/button/button.component';

@Component({
	selector: 'app-root',
	imports: [RouterOutlet, Toast, NgIf, ZardButtonComponent],
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
		public router: Router,
	) {
		this.apiClient.initApi();
	}
}
