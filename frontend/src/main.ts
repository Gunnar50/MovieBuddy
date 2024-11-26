import {bootstrapApplication} from '@angular/platform-browser';

import {AppComponent} from './app/app.component';
import {appConfig} from './app/app.config';

console.log('main.ts: Starting application bootstrap');

bootstrapApplication(AppComponent, appConfig)
  .then(() => {
    console.log('main.ts: Application bootstrapped successfully');
  })
  .catch((err) => {
    console.error('main.ts: Bootstrap failed:', err);
  });
