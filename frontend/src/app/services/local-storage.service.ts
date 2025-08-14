import { Injectable } from '@angular/core';
import { TLocalStorage } from '@entask-types/local-storage/local-storage.type';

@Injectable({
	providedIn: 'root',
})
export class LocalStorageService {
	private storage: Storage = window.localStorage;

	public getAll(): Partial<TLocalStorage> {
		const result: Partial<TLocalStorage> = {};

		(Object.keys(localStorage) as (keyof TLocalStorage)[]).forEach(
			(key: string): void => {
				const value = this.storage.getItem(key);
				if (value !== null) result[key] = value;
			},
		);

		return result;
	}

	public get<K extends keyof TLocalStorage>(key: K): TLocalStorage[K] | null {
		return this.storage.getItem(key) as TLocalStorage[K] | null;
	}

	public static get<K extends keyof TLocalStorage>(
		key: K,
	): TLocalStorage[K] | null {
		return window.localStorage.getItem(key) as TLocalStorage[K] | null;
	}

	public set<K extends keyof TLocalStorage>(
		key: K,
		value: TLocalStorage[K],
	): void {
		this.storage.setItem(key, value);
	}

	public static set<K extends keyof TLocalStorage>(
		key: K,
		value: TLocalStorage[K],
	): void {
		window.localStorage.setItem(key, value);
	}

	public updateMany(values: Partial<TLocalStorage>): void {
		for (const [key, value] of Object.entries(values)) {
			this.storage.setItem(key, value as string);
		}
	}

	public remove<K extends keyof TLocalStorage>(key: K): void {
		this.storage.removeItem(key);
	}

	public clear(): void {
		this.storage.clear();
	}
}
