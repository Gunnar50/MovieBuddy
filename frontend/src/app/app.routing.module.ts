import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

export const ROUTES: Routes = [];

@NgModule({
  imports: [
    RouterModule.forRoot(ROUTES, {
      scrollOffset: [0, 0],
      scrollPositionRestoration: 'top',
    }),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}
