import {DOCUMENT} from '@angular/common';
import {Inject, Injectable} from '@angular/core';
import {Store} from '@ngrx/store';

import * as actions from '../../user/user.actions';
import {CREDENTIALS_KEY, GOOGLE_ID} from '../local_storage';
import {ConfigService} from './config.service';

interface GoogleAuthResponse {
  clientId?: string;
  credential: string;
  select_by?: string;
}

export type GoogleButtonType = 'signIn' | 'signUp';

/**
 * URL of the Sign In With Google client library:
 * https://developers.google.com/identity/gsi/web/guides/overview
 */
export const GSI_CLIENT_URL = 'https://accounts.google.com/gsi/client';

@Injectable({providedIn: 'root'})
export class AuthService {
  constructor(
    @Inject(DOCUMENT) protected readonly document: Document,
    // private readonly store: Store,
    private configService: ConfigService,
  ) {}

  loadGoogleScript(): Promise<void> {
    return new Promise((resolve) => {
      const clientScriptTag = document.createElement('script');
      document.getElementsByTagName('head')[0].appendChild(clientScriptTag);
      clientScriptTag.onload = async () => resolve();
      clientScriptTag.src = GSI_CLIENT_URL;
    });
  }

  async loadClient(): Promise<void> {
    try {
      console.log('Loading Google client...');
      await Promise.all([
        this.loadGoogleScript(),
        this.configService.loadConfig(),
      ]);
      console.log('Google client loaded successfully');
    } catch (error) {
      console.error('Failed to load Google client:', error);
      throw error;
    }
  }

  createGoogleButton(
    wrapperElement: HTMLElement,
    buttonType: GoogleButtonType,
  ) {
    if (!window?.google?.accounts?.id) {
      console.error('Cannot access Google account on window object');
      return;
    }

    const clientId = this.configService.getGoogleClientId();
    if (!clientId) return;

    const googleBtnCallback =
      buttonType === 'signUp'
        ? this.handleSignUp.bind(this)
        : this.handleSignIn.bind(this);

    window.google?.accounts.id.initialize({
      client_id: clientId,
      callback: googleBtnCallback,
    });

    window.google?.accounts.id.renderButton(wrapperElement, {
      shape: 'pill',
      size: 'large',
      text: buttonType === 'signUp' ? 'signup_with' : 'signin_with',
      theme: 'outline',
      type: 'standard',
    });
  }

  private handleSignIn(response: GoogleAuthResponse) {
    localStorage.setItem(CREDENTIALS_KEY, response.credential);
    // this.store.dispatch(
    //   actions.backendLogin({credential: response.credential}),
    // );
  }

  private handleSignUp(response: GoogleAuthResponse) {
    localStorage.setItem(CREDENTIALS_KEY, response.credential);
    const googleId = localStorage.getItem(GOOGLE_ID) || '';
    // this.store.dispatch(
    //   actions.createUser({credential: response.credential, googleId}),
    // );
  }
}
