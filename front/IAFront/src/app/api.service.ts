import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable } from 'rxjs';

@Injectable()
export class ApiService {
  private apiURL = "http://localhost:5000/api/";

  httpOptions = {
    headers: new HttpHeaders({ "Content-Type": "application/json" })
  };

  constructor(private httpClient: HttpClient) {
  }

  getDataForPieChart(): Observable<any> {
    return this.httpClient.get<any>(this.apiURL + "getDataForPieChart/");
  }

  getDataForLineChart(): Observable<any> {
    return this.httpClient.get<any>(this.apiURL + "getDataForLineChart/");
  }

  getWordCloud(): Observable<Blob> {
    return this.httpClient.get<Blob>(this.apiURL + "getWordCloud/" + Date.now(), { responseType: 'blob' as 'json', });
  }

  getCounters(): Observable<any> {
    return this.httpClient.get<any>(this.apiURL + "getCounters/");
  }

  exportCSV(){
    return this.httpClient.get(this.apiURL + "exportCSV/"+ Date.now(), {responseType:'blob'});
  }

  exportExcel(){
    return this.httpClient.get(this.apiURL + "exportExcel/"+ Date.now(), {responseType:'blob'});
  }

  startSearch(query: string): Observable<any> {
    return this.httpClient.get<any>(this.apiURL + "streaming/" + encodeURIComponent(query), this.httpOptions);
  }

  startDemo(query: string): Observable<any> {
    return this.httpClient.get<any>(this.apiURL + "startDemo/" + encodeURIComponent(query), this.httpOptions);
  }

  getTweets(): Observable<any> {
    return this.httpClient.get<any>(this.apiURL + "getTweets/");
  }
}
