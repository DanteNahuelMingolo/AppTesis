import { Component, OnInit, Input } from '@angular/core';
import { DomSanitizer, SafeResourceUrl, SafeUrl } from '@angular/platform-browser';


@Component({
  selector: 'app-wordcloud',
  templateUrl: './wordcloud.component.html',
  styleUrls: ['./wordcloud.component.css']
})
export class WordcloudComponent implements OnInit {
  //data recibida del componente padre
  @Input()
  response: any;

  imageToShow: any;

  //atributo para indicar si se debe mostrar el chart
  //o el mensaje de que no se cargó data aún
  dataLoaded: boolean;


  constructor() {
    //realizamos configuración inicial
    this.initialConfiguration();

    //inicializamos configuración del dataLoaded
    this.setDataLoaded(false);
  }

  ngOnInit(): void {
  }

  ngOnChanges() {
    //si hay data la cargamos en el Chart
    if (this.response && this.response !='data:') {
        this.imageToShow = this.response 

        //si hay data el dataLoaded debe estar en true
        this.setDataLoaded(true);
      } else {
        //si no hay data el dataLoaded debe estar en false
        this.setDataLoaded(false);
      }
  }

  /**
* Configuración inicial
*/
  initialConfiguration() {
    this.imageToShow = ''
  }

  /**
  * Establece si se deberá mostrar el Chart o no
  * @param loaded verdader o falso
  */
  setDataLoaded(loaded: boolean) {
    this.dataLoaded = loaded;
  }


}
