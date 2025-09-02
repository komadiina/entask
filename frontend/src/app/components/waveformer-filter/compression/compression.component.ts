import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { GainEffect } from '@entask-types/dashboard/waveformer-filter.type';

@Component({
	selector: 'app-compression',
	templateUrl: './compression.component.html',
	styleUrl: './compression.component.css',
	changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CompressionComponent {
	@Input() effect!: GainEffect;
}
