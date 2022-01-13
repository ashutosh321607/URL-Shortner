import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroupDirective, NgForm, Validators} from '@angular/forms';
import {ErrorStateMatcher} from '@angular/material/core';
import { NgModule } from '@angular/core';

/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }
}

/** @title Input with a custom ErrorStateMatcher */
@Component({
  selector: 'app-text-box',
  templateUrl: './text-box.component.html',
  styleUrls: ['./text-box.component.css']
})


export class TextBoxComponent implements OnInit {
  isChecked = false;
  urlReg = '(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})[/\\w .-]*/?';

  changed(){
    this.isChecked = !this.isChecked;
  }
  data: URLData = new URLData();

  constructor() { 
  }

  ngOnInit(): void {
  }
  urlFormControl = new FormControl('', [Validators.required, Validators.pattern(this.urlReg)]);
  customUrlFormControl = new FormControl('', [Validators.required, Validators.pattern(this.urlReg)]);
  
  matcher = new MyErrorStateMatcher();
}


class URLData{
  constructor(
    public originalUrl?: string,
    public customUrl?: string
  ) {}
}