import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { LogLevel } from '@entask-constants/logger.constants';
import { TLocalStorage } from '@entask-types/local-storage/local-storage.type';
import { ApiUtil } from '@entask-utilities/api/api.util';
import { LocalStorageService } from '@entask-services/local-storage.service';
import { LoggerService } from '@entask-services/logger.service';
import { RedirectService } from '@entask-services/redirect.service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(
    private redirectService: RedirectService,
    private logService: LoggerService,
    private httpClient: HttpClient,
    private localStorageService: LocalStorageService,
  ) {
    logService.init({ logLevel: LogLevel.DEBUG, logPrefix: 'AuthService' });

    if (this.isLoggedIn() == false) {
      this.redirectService.redirect({ path: '/login' });
    }
  }

  /**
   *
   * @deprecated JWT verification has been implemented on backend, this just provides an additional, minimal layer of security
   */
  public isLoggedIn(): boolean {
    return (
      this.localStorageService.get('accessToken' as keyof TLocalStorage) != null
    );
  }

  public login(username: string, password: string): void {
    this.logService.log([username, password]);
  }

  public async signupGoogle(): Promise<void> {
    const uri = ApiUtil.buildUrl('/public/auth/oauth2');
    this.redirectService.absoluteRedirect(uri);
  }
}
