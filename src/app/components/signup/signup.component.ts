import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { Auth } from 'aws-amplify';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css'],
})
export class SignupComponent implements OnInit {
  email: string = '';
  password: string = '';
  name: string = '';
  confirm_password = '';
  constructor(private router: Router) {}

  emailFormControl = new FormControl('', [
    Validators.required,
    Validators.email,
  ]);

  ngOnInit(): void {}

  register() {
    try {
      const user = Auth.signUp({
        username: this.email,
        password: this.password,
        attributes: {
          email: this.email,
          name: this.name,
        },
      });
      console.log({ user });
      alert('User signup completed , please check verify your email.');
      this.router.navigate(['login']);
    } catch (error) {
      console.log('error signing up:', error);
    }
  }
}
