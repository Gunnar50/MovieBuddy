import {Routes} from '@angular/router';

import {LOGIN_PATH, LOGGED_IN_PATH} from '../utils/routes';

export const routes: Routes = [
  {path: '', redirectTo: LOGIN_PATH, pathMatch: 'full'},
  // {path: LOGIN_PATH, component: LoginComponent},
  // {path: LOGGED_IN_PATH, component: LoggedInComponent},
];
