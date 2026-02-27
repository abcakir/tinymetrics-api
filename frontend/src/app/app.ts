import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  isLoggedIn = false;

  ngOnInit() {
    console.log("🚀 App gestartet. Prüfe Login-Status..");
    this.checkUrlForToken();
  }

  private checkUrlForToken() {
    // 1. Schauen, ob wir gerade von GitHub zurückkommen
    const urlParams = new URLSearchParams(window.location.search);
    const tokenFromUrl = urlParams.get('token');

    if (tokenFromUrl) {
      console.log("Token in der URL gefunden! User wird eingeloggt.");
      localStorage.setItem('token', tokenFromUrl);
      this.isLoggedIn = true;
      
      window.history.replaceState({}, document.title, window.location.pathname);
    } else {
      this.checkStorageForToken();
    }
  }

  private checkStorageForToken() {
    const tokenFromStorage = localStorage.getItem('token');
    if (tokenFromStorage) {
      console.log("User bereits eingeloggt.");
      this.isLoggedIn = true;
    } else {
      console.log("User ist nicht eingeloggt.");
      this.isLoggedIn = false;
    }
  }

  login() {
    console.log("Leite weiter zu GitHub...");
    window.location.href = 'http://localhost:8000/api/v1/auth/github/login';
  }

  logout() {
    console.log("Logge aus...");
    localStorage.removeItem('token');
    this.isLoggedIn = false;
  }
}