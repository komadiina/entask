import * as z from 'zod';

export const registrationResponse = z.object({
	message: z.string(),
});

export type RegistrationResponse = z.infer<typeof registrationResponse>;
