// config.service.ts
import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {firstValueFrom} from 'rxjs';

import {ConfigResponse} from '../../typings/models';

export const CONFIG_ENDPOINT = '/api/config';

@Injectable({
  providedIn: 'root',
})
export class ConfigService {
  private config: ConfigResponse | null = null;

  constructor(private http: HttpClient) {}

  async loadConfig(): Promise<ConfigResponse> {
    if (!this.config) {
      this.config = await firstValueFrom(
        this.http.get<ConfigResponse>(CONFIG_ENDPOINT),
      );
    }
    return this.config;
  }

  getGoogleClientId() {
    if (!this.config) {
      throw new Error('Config is not loaded');
    }
    return this.config.clientId;
  }
}
