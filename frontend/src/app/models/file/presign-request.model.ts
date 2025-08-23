import * as z from 'zod';

export const presignRequest = z.object({
	file: z.file(),
	filename: z.string(),
	conversionType: z.string(),
});

export type PresignRequest = z.infer<typeof presignRequest>;
