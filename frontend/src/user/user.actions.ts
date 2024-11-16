import {createAction, props} from '@ngrx/store';

export const USER_TAG = '[USER]';

export const signIn = createAction(
  `${USER_TAG} Sign In`,
  props<{credentials: string}>(),
);

export const signOut = createAction(`${USER_TAG} Sign Out`);

export const setUserAuth = createAction(`${USER_TAG} Set user auth`);

export const getUser = createAction(`${USER_TAG} Get user`);

export const createUser = createAction(
  `${USER_TAG} Create user`,
  props<{credentials: string; id: string}>(),
);
