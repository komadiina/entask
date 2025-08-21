import { Component, ViewEncapsulation, computed, input } from '@angular/core';
import { ClassValue } from 'clsx';
import { mergeClasses } from '@entask-utils/merge-classes';
import { dropdownShortcutVariants } from './dropdown.variants';

@Component({
	selector: 'z-dropdown-menu-shortcut, [z-dropdown-menu-shortcut]',
	exportAs: 'zDropdownMenuShortcut',
	standalone: true,
	encapsulation: ViewEncapsulation.None,
	template: `<ng-content></ng-content>`,
	host: {
		'[class]': 'classes()',
	},
})
export class ZardDropdownMenuShortcutComponent {
	readonly class = input<ClassValue>('');

	protected readonly classes = computed(() =>
		mergeClasses(dropdownShortcutVariants(), this.class()),
	);
}
