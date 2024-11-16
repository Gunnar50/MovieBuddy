import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {EffectsModule} from '@ngrx/effects';
import {StoreModule} from '@ngrx/store';

import {AppComponent} from './app.component';
import {AppRoutingModule} from './app.routing.module';
import {UserEffects} from '../user/user.effects';
import {userReducer} from '../user/user.reducer';

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,

    EffectsModule.forRoot([UserEffects]),
    StoreModule.forRoot([userReducer]),
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
