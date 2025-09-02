import { Type } from '@angular/core';
import { ChorusComponent } from '@entask-components/waveformer-filter/chorus/chorus.component';
import { CompressionComponent } from '@entask-components/waveformer-filter/compression/compression.component';
import { GainComponent } from '@entask-components/waveformer-filter/gain/gain.component';
import { ReverbComponent } from '@entask-components/waveformer-filter/reverb/reverb.component';

export abstract class BaseEffect {
	constructor(
		public label: string,
		public mix: number,
		public component?: Type<any>,
	) {}
}

export class GainEffect extends BaseEffect {
	constructor(
		public gain: number,
		mix: number,
		label = 'Gain',
	) {
		super(label, mix, GainComponent);
	}
}

export class ChorusEffect extends BaseEffect {
	constructor(
		public rate: number,
		public depth: number,
		mix: number,
		label = 'Chorus',
	) {
		super(label, mix, ChorusComponent);
	}
}

export class ReverbEffect extends BaseEffect {
	constructor(
		public roomSize: number,
		public wet: number,
		public dry: number,
		mix: number,
		label = 'Reverb',
	) {
		super(label, mix, ReverbComponent);
	}
}

export class CompressionEffect extends BaseEffect {
	constructor(
		public attack: number,
		public release: number,
		public threshold: number,
		mix: number,
		label = 'Compression',
	) {
		super(label, mix, CompressionComponent);
	}
}
