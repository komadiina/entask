import {
	BaseEffect,
	ChorusEffect,
	CompressionEffect,
	GainEffect,
	ReverbEffect,
} from '@entask-types/dashboard/waveformer-filter.type';

export const getAvailableFilters = (): BaseEffect[] => [
	new GainEffect(3, 0.5),
	new CompressionEffect(50, 250, -50, 1),
	new ChorusEffect(5, 0.5, 0.5),
	new ReverbEffect(2, 0.5, 0.8, 1),
];
