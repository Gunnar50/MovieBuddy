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
import {ConfigService} from '../utils/services/config.service';

export function resolveGoogleAuthClient(authService: AuthService) {
  return async () => {
    console.log('APP_INITIALIZER: Starting Google client initialization');
    try {
      await authService.loadClient();
      console.log('APP_INITIALIZER: Google client initialized successfully');
    } catch (error) {
      console.error(
        'APP_INITIALIZER: Failed to initialize Google client:',
        error,
      );
      throw error; // This will prevent the app from loading if initialization fails
    }
  };
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
    ConfigService,
    AuthService,
    {
      provide: APP_INITIALIZER,
      useFactory: resolveGoogleAuthClient,
      deps: [AuthService],
      multi: true,
    },
  ],
};
