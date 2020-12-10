import { Component, Input, OnInit } from '@angular/core';
import {Tweet} from '../models/tweet'

@Component({
  selector: 'app-tweet-list',
  templateUrl: './tweet-list.component.html',
  styleUrls: ['./tweet-list.component.css']
})
export class TweetListComponent implements OnInit {
  //data recibida del componente padre
  @Input()
  response: any;

  //atributos necesarios para la lista de tweets
  tweets: Tweet[];

  //atributo para indicar si se debe mostrar el chart
  //o el mensaje de que no se cargó data aún
  dataLoaded: boolean;
  
  /**
  * Configuración y seteo de lo necesario para los tweets
  */
  constructor() { }

  ngOnInit(): void {
  }

  ngOnChanges() {
    //si hay data la cargamos en la lista
    if(this.response){
      if(this.response.data){
        this.tweets = JSON.parse(this.response.data.data);

        //si hay data el dataLoaded debe estar en true
        this.setDataLoaded(true);
      }else{
        //si no hay data el dataLoaded debe estar en false
        this.setDataLoaded(false);
      }
    }
  }

  /**
  * Establece si se deberán mostrar los tweets o no
  * @param loaded verdader o falso
  */
  setDataLoaded(loaded: boolean){
    this.dataLoaded = loaded;
  }
}
