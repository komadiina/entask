import {
	ChangeDetectionStrategy,
	Component,
	ViewEncapsulation,
	computed,
	input,
} from '@angular/core';
import { ClassValue } from 'clsx';
import { mergeClasses } from '@entask-utils/merge-classes';
import { ZardDividerVariants, dividerVariants } from './divider.variants';

@Component({
	selector: 'z-divider',
	standalone: true,
	exportAs: 'zDivider',
	changeDetection: ChangeDetectionStrategy.OnPush,
	encapsulation: ViewEncapsulation.None,
	template: '',
	host: {
		'[attr.role]': `'separator'`,
		'[attr.aria-orientation]': 'zOrientation()',
		'[class]': 'classes()',
	},
})
export class ZardDividerComponent {
	readonly zOrientation =
		input<ZardDividerVariants['zOrientation']>('horizontal');
	readonly zSpacing = input<ZardDividerVariants['zSpacing']>('default');
	readonly class = input<ClassValue>('');

	protected readonly classes = computed(() =>
		mergeClasses(
			dividerVariants({
				zOrientation: this.zOrientation(),
				zSpacing: this.zSpacing(),
			}),
			this.class(),
		),
	);
}
