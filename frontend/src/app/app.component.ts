import {Component} from '@angular/core';
import {RouterOutlet} from '@angular/router';

import {GoogleSignInButtonComponent} from './google-sign-in-button/google-sign-in-button.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, GoogleSignInButtonComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'frontend';
}
