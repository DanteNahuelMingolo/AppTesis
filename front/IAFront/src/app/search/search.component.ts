import { Component, OnInit } from '@angular/core';
import { interval, Observable, Subscription } from 'rxjs';
import { ApiService } from 'src/app/api.service';
import { RealTime } from '../modules/real-time';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  //atributos para el formulario de búsqueda
  wordInput: string;
  maxResultsInput: number;
  countTotal: number;
  countAngry: number;
  countNeutral: number;
  countNotAngry: number;

  //data para los componentes hijos
  public dataChart: any;
  public dataTweets: any;
  public isSearching: any;
  public dataCounters: any;

  //RealTime para data
  dataChartRealTime: RealTime;
  dataTweetsRealTime: RealTime;
  dataCountersRealTime: RealTime;

  /**
  * configuración y seteo de lo necesario
  */
  constructor(public apiService: ApiService) {
    //realizamos la configuración inicial del formulario
    this.initialFormConfiguration();

    //realizamos la configuración inicial de la data
    this.initialDataConfiguration();
  }

  ngOnInit(): void {
  }

  /**
  * Configuración inicial del formulario
  */
  initialFormConfiguration() {
    this.wordInput = "";
    this.maxResultsInput = 3;
    this.countTotal = 0;
    this.countAngry = 0;
    this.countNeutral = 0;
    this.countNotAngry = 0;
  }

  /**
  * Configuración inicial de la data
  */
  initialDataConfiguration() {
    this.dataChart = null;
    this.dataTweets = null;
    this.isSearching = null;
    this.dataCounters = null;
  }

  /**
  * Busca datos en base a los campos del formulario
  */
  search() {
    if (this.wordInput == "" || this.wordInput == null || !(this.maxResultsInput > 0)) {
      alert("Todos los campos son obligatorios");
    } else {
      //obtenemos los datos para los chart
      // this.getDataChart();
      this.startDataChartRealTime();

      //iniciamos la búsqueda
      this.startSearch();
      //obtenemos los datos para los tweets
      this.startDataTweetsRealTime();
      //actualizo los contadores
      this.startDataCountersRealTime()
    }
  }

  /**
  * Obtiene los datos para los chart
  */
  getDataChart() {
    this.apiService.getDataForPieChart().subscribe(result => {
      this.dataChart = result;
    });
  }

  /**
  * Obtiene los datos para los chart
  */
  startSearch() {
    this.apiService.startSearch(this.wordInput).subscribe(result => {
      this.isSearching = result;
    });
  }

  /**
  * Obtiene los datos para los tweets
  */
  getTweets() {
    this.apiService.getTweets().subscribe(result => {
      this.dataTweets = result;
    });
  }

  /**
  * Inicia el RealTime para dataChart
  */
  startDataChartRealTime() {
    //como la función que quiero enviar al RealTime usa el apiserver debo enviar todo el módulo
    var context = this;
    var functionToExecute = function () {
      context.apiService.getDataForPieChart().subscribe(result => {
        context.dataChart = result;
      });
    };

    this.dataChartRealTime = new RealTime(3000, functionToExecute);
  }

  startDataCountersRealTime(){
    var context = this;
    var functionToExecute = function (){
      context.apiService.getCounters().subscribe(result =>{
        context.countAngry = result.data.data.countAggresive;
        context.countNeutral = result.data.data.countNeutral;
        context.countNotAngry = result.data.data.countNonAggresive;
        context.countTotal = result.data.data.countTotal;
      });
    };

    this.dataCountersRealTime = new RealTime(3000,functionToExecute)
  }

  /**
  * Inicia el RealTime para dataTweets
  */
  startDataTweetsRealTime() {
    //como la función que quiero enviar al RealTime usa el apiserver debo enviar todo el módulo
    var context = this;
    var functionToExecute = function () {
      context.apiService.getTweets().subscribe(result => {
        context.dataTweets = result;
      });
    };

    this.dataTweetsRealTime = new RealTime(3000, functionToExecute);
  }

  /**
  * Detiene el RealTime para dataTweets
  */
  stopDataTweetsRealTime() {
    this.dataTweetsRealTime.stop();
  }
  /**
  * Detiene el RealTime para dataChart
  */
  stopDataChartRealTime() {
    this.dataChartRealTime.stop();
  }

}
