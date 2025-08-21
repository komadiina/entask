import {
	Component,
	TemplateRef,
	ViewChild,
	ViewEncapsulation,
	computed,
	input,
} from '@angular/core';
import { ClassValue } from 'clsx';
import { mergeClasses } from '@entask-utils/merge-classes';
import { dropdownContentVariants } from './dropdown.variants';

@Component({
	selector: 'z-dropdown-menu-content',
	exportAs: 'zDropdownMenuContent',
	standalone: true,
	encapsulation: ViewEncapsulation.None,
	template: `
		<ng-template #contentTemplate>
			<div
				[class]="contentClasses()"
				role="menu"
				tabindex="-1"
				[attr.aria-orientation]="'vertical'"
			>
				<ng-content></ng-content>
			</div>
		</ng-template>
	`,
})
export class ZardDropdownMenuContentComponent {
	@ViewChild('contentTemplate', { static: true })
	contentTemplate!: TemplateRef<unknown>;

	readonly class = input<ClassValue>('');

	protected readonly contentClasses = computed(() =>
		mergeClasses(dropdownContentVariants(), this.class()),
	);
}
