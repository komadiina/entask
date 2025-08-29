import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { TFileConversionForm } from '@entask-types/dashboard/forms.type';
import { Observable, firstValueFrom, lastValueFrom } from 'rxjs';
import { PresignRequest } from '@entask-models/file/presign-request.model';
import { PresignResponse } from '@entask-models/file/presign-response.model';
import { LocalStorageService } from '@entask-services/local-storage.service';
import { ApiUtil } from '@entask-utils/api/api.util';

@Injectable({
	providedIn: 'root',
})
export class DashboardService {
	constructor(private http: HttpClient) {}

	public async getSignedUrl(
		body: PresignRequest,
		file: File,
	): Promise<PresignResponse> {
		const endpoint = ApiUtil.builder()
			.service('file')
			.endpoint('/presign/upload')
			.build();

		return await firstValueFrom(
			this.http.get<PresignResponse>(endpoint, {
				headers: {
					'Content-Length': file.size.toString(),
					'Content-Type': file.type,
				},
				params: {
					filename: body.filename,
					conversion_type: body.conversionType,
					file_mime_type: body.file!.type,
				},
			}),
		);
	}

	public async uploadFile<T extends TFileConversionForm>(
		presignDetails: PresignResponse,
		data: T,
	): Promise<any> {
		const endpoint = presignDetails.url;

		// amends auth headers via httpinterceptor -> breaks presign upload flow
		// return await firstValueFrom(this.http.put(endpoint, data.content!));

		// avoids httpInterceptors -> minio works, no auth headers needed for presigned url
		return await fetch(endpoint, {
			method: 'PUT',
			body: data.content!,
			window: null,
		});
	}

	public async submitConversionRequest(
		data: any, // TODO: implement type -> {...body, objectKey} cba atm
	): Promise<any> {
		const endpoint = ApiUtil.builder()
			.service('conversion')
			.endpoint('/submit')
			.build();

		return await lastValueFrom(
			this.http.post(endpoint, {
				...data,
				type: data.conversionType,
				clientId: LocalStorageService.get('uuid'),
			}),
		);
	}

	public cancelConversion(): Observable<any> {
		const endpoint = ApiUtil.builder()
			.service('conversion')
			.endpoint(LocalStorageService.get('workflowId')!)
			.queryParam('client_id', LocalStorageService.get('uuid')!)
			.build();

		return this.http.delete<any>(endpoint);
	}
	private parseFilename(cd: string | null, url: string): string {
		if (cd) {
			const m1 = cd.match(/filename\*=UTF-8''([^;]+)/i);
			if (m1) return decodeURIComponent(m1[1]);
			const m2 = cd.match(/filename="?([^";]+)"?/i);
			if (m2) return m2[1];
		}
		try {
			const u = new URL(url);
			return (
				u.searchParams
					.get('response-content-disposition')
					?.split('filename=')[1] ??
				(u.pathname.split('/').pop() || 'download')
			);
		} catch {
			return 'download';
		}
	}

	public async downloadResult(url: string): Promise<void> {
		const resp = await fetch(url, {
			method: 'GET',
			mode: 'cors',
			credentials: 'omit',
		});

		if (!resp.ok) {
			throw new Error(`HTTP error! status: ${resp.status}`);
		}

		const blob = await resp.blob();
		const filename = this.parseFilename(
			resp.headers.get('content-disposition'),
			url,
		);

		const objectUrl = URL.createObjectURL(blob);

		const a = document.createElement('a');
		a.href = objectUrl;
		a.download = filename;
		document.body.appendChild(a);
		a.click();
		a.remove();

		URL.revokeObjectURL(objectUrl);
	}
}
