import { NgIf } from '@angular/common';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

@Component({
	selector: 'app-backwards-arrow',
	imports: [NgIf],
	templateUrl: './backwards-arrow.component.html',
	styleUrl: './backwards-arrow.component.css',
	changeDetection: ChangeDetectionStrategy.OnPush,
})
export class BackwardsArrowComponent {
	@Input({ required: true }) history!: History;

	navigateBackward(): void {
		this.history.back();
	}

	notRoot(): boolean {
		return (
			window.location.pathname != '/' && window.location.pathname != '/login'
		);
	}
}
