import * as z from 'zod';

export const presignResponse = z.object({
	url: z.string(),
	bucket: z.string(),
	key: z.string(),
	userId: z.string().optional(),
});

export type PresignResponse = z.infer<typeof presignResponse>;
