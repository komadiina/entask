import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {
	TFileConversionForm,
} from '@entask-types/dashboard/forms.type';
import { firstValueFrom, lastValueFrom } from 'rxjs';
import { PresignRequest } from '@entask-models/file/presign-request.model';
import { PresignResponse } from '@entask-models/file/presign-response.model';
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
			.breadcrumbs('presign', 'upload')
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
		});
	}

	public async submitConversionRequest(
		data: any, // TODO: implement type -> {...body, objectKey} cba atm
	): Promise<any> {
		const endpoint = ApiUtil.builder()
			.service('conversion')
			.breadcrumbs('submit')
			.build();

		return await lastValueFrom(
			this.http.post(endpoint, { ...data, type: data.conversionType }),
		);
	}
}
