import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { BackwardsArrowComponent } from './components/backwards-arrow/backwards-arrow.component';
import { APIService } from './services/api.service';

@Component({
	selector: 'app-root',
	imports: [RouterOutlet, BackwardsArrowComponent],
	templateUrl: './app.component.html',
	styleUrl: './app.component.css',
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
