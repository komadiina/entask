import { NgIf } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { Router } from '@angular/router';
import { ZardButtonComponent } from '../button/button.component';

@Component({
	selector: 'app-header',
	imports: [ZardButtonComponent, NgIf],
	templateUrl: './header.component.html',
	styleUrl: './header.component.css',
	changeDetection: ChangeDetectionStrategy.OnPush,
	standalone: true,
})
export class HeaderComponent {
	constructor(public router: Router) {}
}
