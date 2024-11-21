import {bootstrapApplication} from '@angular/platform-browser';

import {AppComponent} from './app/app.component';
import {appConfig} from './app/app.config';

debugger; // This should pause execution if DevTools is open
console.log('main.ts: Starting application bootstrap');

bootstrapApplication(AppComponent, appConfig)
  .then(() => {
    debugger;
    console.log('main.ts: Application bootstrapped successfully');
  })
  .catch((err) => {
    debugger;
    console.error('main.ts: Bootstrap failed:', err);
  });
