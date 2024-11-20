import {provideHttpClient} from '@angular/common/http';
import {
  APP_INITIALIZER,
  ApplicationConfig,
  provideZoneChangeDetection,
} from '@angular/core';
import {provideRouter} from '@angular/router';
import {provideStoreDevtools} from '@ngrx/store-devtools';

import {routes} from './app.routes';
import {AuthService} from '../utils/services/auth.service';

export function resolveGoogleAuthClient(authService: AuthService) {
  return () => authService.loadClient();
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    provideZoneChangeDetection({eventCoalescing: true}),
    provideRouter(routes),
    provideStoreDevtools({
      maxAge: 25,
      logOnly: true,
      autoPause: true,
    }),
    {
      provide: AuthService,
      useClass: AuthService,
    },
    {
      provide: APP_INITIALIZER,
      useFactory: resolveGoogleAuthClient,
      deps: [AuthService],
      multi: true,
    },
  ],
};
