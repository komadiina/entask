import * as z from 'zod';

export const loginResponse = z.object({
	accessToken: z.string(),
	refreshToken: z.string(),
	idToken: z.string(),
	accessTokenExpiry: z.string(),
	refreshTokenExpiry: z.string(),
});

export type LoginResponse = z.infer<typeof loginResponse>;
