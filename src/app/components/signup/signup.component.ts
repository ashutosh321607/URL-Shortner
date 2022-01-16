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
      }).then(
        (data) => {
          console.log('SignUp Success', data);
          this.router.navigate(['/signin']);
        }
      )
      console.log({ user });
      alert('User signup completed , please check verify your email.');
      this.router.navigate(['signin']);
    } catch (error) {
      console.log('error signing up:', error);
    }
  }

  OnSignUpClick() {
    this.register();
  }
}
