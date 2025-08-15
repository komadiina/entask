export interface TLocalStorage {
  idToken: string;
	accessToken: string;
	refreshToken: string;
  apiVersion: string;
}

export type KLocalStorage = keyof TLocalStorage;
export type VLocalStorage = TLocalStorage[KLocalStorage];
