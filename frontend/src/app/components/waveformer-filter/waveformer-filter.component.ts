import { NgForOf } from '@angular/common';
import { ChangeDetectionStrategy, Component, ViewChild } from '@angular/core';
import { ZardButtonComponent } from '@entask-components/button/button.component';
import { ZardDropdownModule } from '@entask-components/dropdown/dropdown.module';
import { EntaskDirectivesModule } from '@entask-directives/directives.module';
import { BaseEffect } from '@entask-types/dashboard/waveformer-filter.type';
import { EffectHostDirective } from '@entask-root/directives/effect-host.directive';
import { getAvailableFilters } from '@entask-utils/dashboard/waveformer/available-filters';

@Component({
	selector: 'app-waveformer-filter',
	templateUrl: './waveformer-filter.component.html',
	styleUrl: './waveformer-filter.component.css',
	changeDetection: ChangeDetectionStrategy.OnPush,
	imports: [
		ZardDropdownModule,
		NgForOf,
		ZardButtonComponent,
		EntaskDirectivesModule,
	],
	standalone: true,
})
export class WaveformerFilterComponent {
	readonly availableFilters: BaseEffect[] = getAvailableFilters();
	filters: BaseEffect[] = [];

	@ViewChild(EffectHostDirective, { static: true })
	effectHost!: EffectHostDirective;

	render(effect: BaseEffect) {
		const vcr = this.effectHost.vcref;
		vcr.clear();

		const cmpRef = vcr.createComponent(effect.component!);
		(cmpRef.instance as any).effect = effect;
		cmpRef.changeDetectorRef.detectChanges();
	}
}
