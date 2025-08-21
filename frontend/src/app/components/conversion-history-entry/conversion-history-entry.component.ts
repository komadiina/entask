import { DatePipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

@Component({
	selector: 'app-conversion-history-entry',
	imports: [DatePipe],
	templateUrl: './conversion-history-entry.component.html',
	styleUrl: './conversion-history-entry.component.css',
	changeDetection: ChangeDetectionStrategy.OnPush,
	standalone: true,
})
export class ConversionHistoryEntryComponent {
	@Input({ required: true }) entry!: any;
}
