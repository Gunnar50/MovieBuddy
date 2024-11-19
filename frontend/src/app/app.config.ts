import {
  APP_INITIALIZER,
  ApplicationConfig,
  provideZoneChangeDetection,
} from '@angular/core';
import {provideClientHydration} from '@angular/platform-browser';
import {provideRouter, withRouterConfig} from '@angular/router';
import {provideStoreDevtools} from '@ngrx/store-devtools';

import {routes} from './app.routes';
import {AuthService} from '../utils/services/auth.service';

export function resolveGoogleAuthClient(AuthService: AuthService) {
  return () => AuthService.loadClient();
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({eventCoalescing: true}),
    provideRouter(routes),
    provideClientHydration(),
    provideStoreDevtools({
      maxAge: 25,
      logOnly: true,
      autoPause: true,
    }),
    AuthService,
    {
      provide: APP_INITIALIZER,
      useFactory: resolveGoogleAuthClient,
      deps: [AuthService],
      multi: true,
    },
  ],
};
