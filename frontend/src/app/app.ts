import { Component, OnInit, ChangeDetectorRef} from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

interface UrlEntry {
  id: number;
  short_code: string;
  original_url: string;
  click_count: number;
  created_at?: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  isLoggedIn = false;
  email = '';
  password = '';
  signupEmail = '';
  signupPassword = '';
  urls: UrlEntry[] = [];
  newUrl = '';

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    console.log("🚀 App gestartet. Prüfe Login-Status..");
    this.checkUrlForToken();
  }

  private getAuthHeaders() {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  private loadUrls() {
    this.http.get<UrlEntry[]>('https://tinymetrics.duckdns.org/api/v1/urls/me', { headers: this.getAuthHeaders() })
      .subscribe({
        next: (data) => {
          this.urls = data;
          this.cdr.detectChanges();
        },
        error: (err) => console.error("Konnte URLs nicht laden", err)
      });
  }

  shortenUrl() {
    if (!this.newUrl) return; 
    this.http.post<UrlEntry>('https://tinymetrics.duckdns.org/api/v1/urls/', 
      { original_url: this.newUrl }, 
      { headers: this.getAuthHeaders() }
    ).subscribe({
        next: (data) => {
          this.urls.unshift(data); 
          this.newUrl = '';
          this.cdr.detectChanges();
        },
        error: (err) => {
          console.error("Fehler:", err);
          alert("Das hat nicht geklappt!");
        }
      });
  }

  private checkUrlForToken() {
    // 1. Schauen, ob wir gerade von GitHub zurückkommen
    const urlParams = new URLSearchParams(window.location.search);
    const tokenFromUrl = urlParams.get('token');

    if (tokenFromUrl) {
      console.log("Token in der URL gefunden! User wird eingeloggt.");
      localStorage.setItem('token', tokenFromUrl);
      this.isLoggedIn = true;
      this.loadUrls();
      
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
      this.loadUrls();
    } else {
      console.log("User ist nicht eingeloggt.");
      this.isLoggedIn = false;
    }
  }

  login() {
    console.log("Leite weiter zu GitHub...");
    window.location.href = 'https://tinymetrics.duckdns.org/api/v1/auth/github/login';
  }

  logout() {
    console.log("Logge aus...");
    localStorage.removeItem('token');
    this.isLoggedIn = false;
  }

  loginWithPassword(){
    const body = new URLSearchParams();
    body.set('username', this.email);
    body.set('password', this.password);

    const headers = new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' });
    this.http.post<any>('https://tinymetrics.duckdns.org/api/v1/auth/login', body.toString(), { headers })
      .subscribe({
        next: (response) => {
          console.log("✅ Passwort-Login erfolgreich!");
          localStorage.setItem('token', response.access_token);
          this.isLoggedIn = true;
          this.loadUrls();
        },
        error: (err) => {
          console.error("Login fehlgeschlagen:", err);
          alert("Falsche E-Mail oder Passwort!");
        }
      });
  }

  signup() {
    this.http.post<{ id: number; email: string }>(
      'https://tinymetrics.duckdns.org/api/v1/auth/register',
      { email: this.signupEmail, password: this.signupPassword },
      { headers: { 'Content-Type': 'application/json' } }
    ).subscribe({
      next: () => {
        console.log("✅ Registrierung erfolgreich!");
        alert("Registrierung erfolgreich! Du kannst dich jetzt einloggen.");
        this.signupEmail = '';
        this.signupPassword = '';
      },
      error: (err) => {
        console.error("Signup fehlgeschlagen:", err);
        const msg = err.error?.detail ?? "Registrierung fehlgeschlagen.";
        alert(typeof msg === 'string' ? msg : JSON.stringify(msg));
      }
    });
  }

copyToClipboard(shortCode: string) {
  const fullUrl = `https://tinymetrics.duckdns.org/${shortCode}`;
  navigator.clipboard.writeText(fullUrl).then(() => {
    alert("Link in die Zwischenablage kopiert!");
  });
}
}