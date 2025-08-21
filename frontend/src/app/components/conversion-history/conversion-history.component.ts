import { AsyncPipe, NgFor, NgForOf, NgIf } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { from, map } from 'rxjs';
import { Observable } from 'rxjs';
import { ConversionHistoryEntryComponent } from '../conversion-history-entry/conversion-history-entry.component';

@Component({
	selector: 'app-conversion-history',
	templateUrl: './conversion-history.component.html',
	styleUrl: './conversion-history.component.css',
	changeDetection: ChangeDetectionStrategy.OnPush,
	standalone: true,
	imports: [NgIf, NgForOf, NgFor, AsyncPipe, ConversionHistoryEntryComponent],
})
export class ConversionHistoryComponent {
	history$: Observable<any[]> | null = null;

	constructor() {
		this.history$ = from(import('@public/dummy/profile.json')).pipe(
			map((data) => data.default.history),
		);
	}
}
