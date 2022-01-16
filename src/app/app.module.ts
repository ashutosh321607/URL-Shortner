import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { TextBoxComponent } from './components/text-box/text-box.component';
import { HeaderComponent } from './components/header/header.component';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ClipboardComponent } from './components/clipboard/clipboard.component';
import { ClipboardModule } from '@angular/cdk/clipboard';
import { MatCardModule } from '@angular/material/card';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { SignupComponent } from './components/signup/signup.component';
import { SigninComponent } from './components/signin/signin.component';
import { LandingPageComponent } from './components/landing-page/landing-page.component';
import Amplify, { Auth } from 'aws-amplify';

Amplify.configure({
  Auth: {
    mandatorySignIn: true,
    region: 'ap-south-1',
    userPoolId: 'ap-south-1_dtuSSUhxg',
    userPoolWebClientId: '67q3k6h8j5uq31r5ouicsel9b1',
    authenticationFlowType: 'ALLOW_REFRESH_TOKEN_AUTH',
  },
});

@NgModule({
  declarations: [
    AppComponent,
    TextBoxComponent,
    HeaderComponent,
    ClipboardComponent,
    SignupComponent,
    SigninComponent,
    LandingPageComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatIconModule,
    MatToolbarModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    FormsModule,
    ReactiveFormsModule,
    ClipboardModule,
    MatCardModule,
    MatSlideToggleModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
