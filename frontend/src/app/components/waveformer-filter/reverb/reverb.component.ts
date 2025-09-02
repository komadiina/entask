import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { ReverbEffect } from '@entask-types/dashboard/waveformer-filter.type';

@Component({
	selector: 'app-reverb',
	templateUrl: './reverb.component.html',
	styleUrl: './reverb.component.css',
	changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ReverbComponent {
	@Input() effect!: ReverbEffect;

	constructor() {
		console.log('ReverbComponent');
	}
}
