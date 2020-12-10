import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable } from 'rxjs';

@Injectable()
export class ApiService {
  //private apiURL = "http://fatalblack.pythonanywhere.com/api/";
  private apiURL = "http://localhost:5000/api/";

  httpOptions = {
    headers: new HttpHeaders({ "Content-Type": "application/json" })
  };
  
  constructor(private httpClient : HttpClient)
  {
  }

  getDataForPieChart (word: string): Observable<any> {
    return this.httpClient.get<any>(this.apiURL + "dataForPieChart/" + word);
  }

  getTwitts (word: string, maxResults: number): Observable<any> {
    return this.httpClient.get<any>(this.apiURL + "searchTwitts/" + word + "/" + maxResults);
  }

  startSearch (query:string):Observable<any>{
     return this.httpClient.get<any>(this.apiURL + "streaming/"+ query, this.httpOptions );
  }

  getTweets (): Observable<any>{
    return this.httpClient.get<any>(this.apiURL + "getTweets/");
  }
}
