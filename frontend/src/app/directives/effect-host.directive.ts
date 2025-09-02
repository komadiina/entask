import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
	selector: '[effectHost]',
	exportAs: 'effectHost',
	standalone: true,
})
export class EffectHostDirective {
	constructor(public vcref: ViewContainerRef) {}
}
