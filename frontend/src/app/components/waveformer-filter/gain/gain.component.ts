import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { GainEffect } from '@entask-types/dashboard/waveformer-filter.type';

@Component({
  selector: 'app-gain',
  templateUrl: './gain.component.html',
  styleUrl: './gain.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class GainComponent { 
  @Input() effect!: GainEffect;
}
