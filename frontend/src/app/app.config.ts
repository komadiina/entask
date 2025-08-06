import { registerLocaleData } from '@angular/common';
import { provideHttpClient } from '@angular/common/http';
import en from '@angular/common/locales/en';
import {
	ApplicationConfig,
	importProvidersFrom,
	provideZoneChangeDetection,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideRouter } from '@angular/router';
import Aura from '@primeng/themes/aura';
import { en_US, provideNzI18n } from 'ng-zorro-antd/i18n';
import { provideNzIcons } from 'ng-zorro-antd/icon';
import { MessageService } from 'primeng/api';
import { providePrimeNG } from 'primeng/config';
import { routes } from './app.routes';
import { icons } from './icons-provider';

registerLocaleData(en);

export const appConfig: ApplicationConfig = {
	providers: [
		provideHttpClient(),
		provideRouter(routes),
		provideZoneChangeDetection({ eventCoalescing: true }),
		provideNzIcons(icons),
		importProvidersFrom(FormsModule),
		provideNzI18n(en_US),
		provideAnimationsAsync(),
		providePrimeNG({
			theme: {
				preset: Aura,
				options: {
					darkModeSelector: '', // jedini workaround da forsiram tamnu temu ???
					cssLayer: {
						name: 'primeng',
						order: 'theme, base, primeng',
					},
				},
			},
		}),
		MessageService,
	],
};
