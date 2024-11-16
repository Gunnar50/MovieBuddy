import {Action, createReducer, on} from '@ngrx/store';

import * as actions from './user.actions';

export interface UserState {
  isAuth: boolean;
}

export const INITIAL_STATE: UserState = {
  isAuth: false,
};

export const reducer = createReducer(
  INITIAL_STATE,
  on(actions.setUserAuth, (state): UserState => {
    return {
      ...state,
      isAuth: true,
    };
  }),
);

export function userReducer(state: UserState, action: Action): UserState {
  return reducer(state, action);
}
