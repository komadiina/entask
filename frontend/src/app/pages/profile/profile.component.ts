import { AsyncPipe, DatePipe, NgIf } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { Observable, from, map } from 'rxjs';
import { ConversionHistoryComponent } from '@entask-root/components/conversion-history/conversion-history.component';
import { HeaderComponent } from '@entask-root/components/header/header.component';
import { ZardLoaderComponent } from '@entask-root/components/loader/loader.component';

@Component({
	selector: 'app-profile',
	imports: [
		NgIf,
		AsyncPipe,
		DatePipe,
		ZardLoaderComponent,
		ConversionHistoryComponent,
		HeaderComponent,
	],
	templateUrl: './profile.component.html',
	styleUrl: './profile.component.css',
	changeDetection: ChangeDetectionStrategy.OnPush,
	standalone: true,
})
export class ProfileComponent {
	user$: Observable<any>;

	public constructor() {
		this.user$ = from(import('@public/dummy/profile.json')).pipe(
			map((data) => data.default),
		);
	}
}
