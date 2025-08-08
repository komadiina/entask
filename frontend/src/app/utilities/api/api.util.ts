import { environment } from '@entask-environments/environment';

export class ApiUtil {
	public static buildUrl(path: string): string {
		return `${environment.backendUrl}/${localStorage.getItem('apiVersion')}${path}`;
	}
}
