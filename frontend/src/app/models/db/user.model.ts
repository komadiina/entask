import * as z from 'zod';

export const user = z.object({
	id: z.number(),
	username: z.string(),
	email: z.string(),
	password: z.string(),
	givenName: z.string(),
	familyName: z.string(),
});

export type User = z.infer<typeof user>;
