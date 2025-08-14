import { Observer } from 'rxjs';

export class BaseObserver<T, C = unknown> implements Observer<T> {
	protected ctx: C | null = null;

	public constructor(
		private onNext: (value: T, ctx: C | null) => void,
		private onError: (error: Error, ctx: C | null) => void,
		private onComplete: (ctx: C | null) => void,
	) {}

	public context(component: C): BaseObserver<T, C> {
		this.ctx = component;
		return this;
	}

	public next(value: T): void {
		this.onNext(value, this.ctx);
	}

  public error(error: Error): void {
    
		this.onError(error, this.ctx);
	}

	public complete(): void {
		this.onComplete(this.ctx);
	}
}
