import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

let API_URL = 'http://localhost:5000/';

@Injectable({
  providedIn: 'root',
})
export class HandleApiService {
  constructor(private http: HttpClient) {}

  post_api(original_url: string) {
    return this.http
      .post(API_URL + 'post_profile_data', {
        username: 'test',
        password: 'test',
        original_url: original_url,
      });
  }

  get_api(username: string, password: string) {
    return this.http.post(API_URL + 'get_profile_data', {
      username: username,
      password: password,
    });
  }
}
