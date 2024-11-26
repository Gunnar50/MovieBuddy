import {
  ChangeDetectionStrategy,
  Component,
  effect,
  ElementRef,
  input,
  viewChild,
} from '@angular/core';

import {AuthService, GoogleButtonType} from '../../utils/services/auth.service';

@Component({
  selector: 'app-google-sign-in-button',
  templateUrl: './google-sign-in-button.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  standalone: true,
  imports: [],
})
export class GoogleSignInButtonComponent {
  readonly isShort = input<boolean>(false);
  readonly googleButtonType = input.required<GoogleButtonType>();
  readonly signInButtonElement =
    viewChild<ElementRef<HTMLDivElement>>('signInButton');

  constructor(private readonly authService: AuthService) {
    effect(() => {
      try {
        const signInButtonElement = this.signInButtonElement()?.nativeElement;

        if (signInButtonElement) {
          this.authService.createGoogleButton(
            signInButtonElement,
            this.googleButtonType(),
          );
        }
      } catch (error) {
        console.error('Error in Google Sign In button effect:', error);
      }
    });
  }
}
