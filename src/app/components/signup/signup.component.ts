import { Component, OnInit } from '@angular/core';
import {FormControl, Validators} from '@angular/forms';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
// export class SignupComponent implements OnInit {

//   constructor() { }

//   ngOnInit(): void {
//   }

// }
export class SignupComponent {
  emailFormControl = new FormControl('', [
    Validators.required,
    Validators.email,
  ]);
}