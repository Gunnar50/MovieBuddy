/** Used to store the url to redirect the user to after authenticating */
export const REDIRECT_URL_KEY = 'redirectUrl';

export function clearLocalStorage() {
  localStorage.clear();
}

/** Used to store Google JWT credentials after successful sign-in. */
export const CREDENTIALS_KEY = 'credentials';
export const GOOGLE_ID = 'google_id';
