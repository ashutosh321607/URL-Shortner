import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { HttpHeaders } from '@angular/common/http';
import { HttpParams } from '@angular/common/http';

let API_URL = '';

@Injectable({
  providedIn: 'root',
})
export class HandleApiService {
  constructor(private http: HttpClient) {}

  post_api(original_url: string, username: string, password: string) {
    const api_url = `/post_profile_data?username=${username}&password=${password}&original_url=${original_url}` ;
    const promise = this.http.get(api_url).toPromise();
    return promise;
  }

  post_api_with_custom(original_url: string, username: string, password: string, custom_url: string) {
    const api_url = `/post_profile_data?username=${username}&password=${password}&original_url=${original_url}&custom_shorten_url=${custom_url}` ;
    const promise = this.http.get(api_url).toPromise();
    return promise;
  }
  
  get_api(username: string, password: string) {
    const api_url = `/get_profile_data?username=${username}&password=${password}` ;
    const promise = this.http.get(api_url).toPromise();
    return promise;
  }
}
