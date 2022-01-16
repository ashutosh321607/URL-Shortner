import { Component, OnInit } from '@angular/core';
import {FormControl, Validators} from '@angular/forms';
import { Router } from '@angular/router';
import { Auth} from 'aws-amplify';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent implements OnInit{
  email: string = '';
  password: string = '';

  OnSignIn(){
    this.loginWithCognito();
  }

  constructor(private router: Router) { }
  ngOnInit(): void {
  }
  emailFormControl = new FormControl('', [
    Validators.required,
    Validators.email,
  ]);
  async loginWithCognito() {
        try {
          var user = await Auth.signIn(this.email.toString(), this.password.toString());
          console.log('Authentication performed for user=' + this.email + 'password=' + this.password + ' login result==' + user);
          var tokens = user.signInUserSession;
          if (tokens != null) {
            console.log('User authenticated');
            this.router.navigate(['home']);
            alert('You are logged in successfully !');
          }
        } catch (error) {
          console.log(error);
          alert('User Authentication failed');
        }
      }
}
