import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { HttpHeaders } from '@angular/common/http';
import { HttpParams } from '@angular/common/http';

let API_URL = 'http://localhost:5000/';

@Injectable({
  providedIn: 'root',
})
export class HandleApiService {
  constructor(private http: HttpClient) {}

  post_api(original_url: string) {
    const api_url = `http://localhost:5000/post_profile_data?username=myusername&password=mypassword&original_url=${original_url}` ;
    const promise = this.http.get(api_url).toPromise();
    return promise;
  }

  get_api(username: string, password: string) {
    return this.http.post('get_profile_data', {
      username: username,
      password: password,
    });
  }
}
