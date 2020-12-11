import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable } from 'rxjs';

@Injectable()
export class ApiService {
  private apiURL = "http://localhost:5000/api/";

  httpOptions = {
    headers: new HttpHeaders({ "Content-Type": "application/json" })
  };
  
  constructor(private httpClient : HttpClient)
  {
  }

  getDataForPieChart (query: string): Observable<any> {
    return this.httpClient.get<any>(this.apiURL + "dataForPieChart/" + encodeURIComponent(query));
  }

  getTwitts (query: string, maxResults: number): Observable<any> {
    return this.httpClient.get<any>(this.apiURL + "searchTwitts/" +encodeURIComponent(query) + "/" + maxResults);
  }

  startSearch (query:string):Observable<any>{
     return this.httpClient.get<any>(this.apiURL + "streaming/"+ encodeURIComponent(query), this.httpOptions );
  }

  getTweets (): Observable<any>{
    return this.httpClient.get<any>(this.apiURL + "getTweets/");
  }
}
