import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { ChorusEffect } from '@entask-types/dashboard/waveformer-filter.type';

@Component({
	selector: 'app-chorus',
	templateUrl: './chorus.component.html',
	styleUrl: './chorus.component.css',
	changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ChorusComponent {
	@Input() effect!: ChorusEffect;
}
