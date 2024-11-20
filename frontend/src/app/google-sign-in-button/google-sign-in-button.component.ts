import {
  ChangeDetectionStrategy,
  Component,
  computed,
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
      const signInButtonElement = this.signInButtonElement()?.nativeElement;

      if (signInButtonElement) {
        this.authService.createGoogleButton(
          signInButtonElement,
          this.googleButtonType(),
        );
      }
    });
  }
}
