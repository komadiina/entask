export interface TBaseConversionForm {
	contentType: string;
	content?: File | string;
}

export interface TFileConversionForm extends TBaseConversionForm {
	description?: string | null;
	resultName?: string;
	file?: File;
	formData?: FormData;
	conversionType: string;
}

export interface WaveformerForm extends TFileConversionForm {
	filters?: {
		compress: boolean;
		reverb: boolean;
		gain: boolean;
		downmix: boolean;
	};
}

export interface TermExtractorForm extends TBaseConversionForm {
	text?: string;
}
