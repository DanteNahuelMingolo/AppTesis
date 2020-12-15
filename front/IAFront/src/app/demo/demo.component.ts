import { Component, OnInit, Pipe, PipeTransform } from '@angular/core';
import { ApiService } from 'src/app/api.service';
import { RealTime } from '../modules/real-time';
import { saveAs } from 'file-saver';

@Component({
  selector: 'app-demo',
  templateUrl: './demo.component.html',
  styleUrls: ['./demo.component.css']
})
export class DemoComponent implements OnInit {
  //atributos para el formulario de búsqueda
  wordInput: string;
  maxResultsInput: number;
  countTotal: number;
  countAngry: number;
  countNeutral: number;
  countNotAngry: number;

  //data para los componentes hijos
  public dataPieChart: any;
  public dataLineChart: any;
  public dataTweets: any;
  public isSearching: any;
  public dataCounters: any;
  public imageToShow: any;
  public isImageLoading: boolean;

  //RealTime para data
  dataPieChartRealTime: RealTime;
  dataLineChartRealTime: RealTime;
  dataTweetsRealTime: RealTime;
  dataCountersRealTime: RealTime;
  dataWordCloudRealTime: RealTime;

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

  ngOnDestroy(){
    this.stopChartsRealTime();
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
    this.dataPieChart = null;
    this.dataLineChart = null;
    this.dataTweets = null;
    this.isSearching = null;
    this.dataCounters = null;
    this.imageToShow = null;
  }

  exportCSV() {
    this.apiService.exportCSV().subscribe(data => saveAs(data, `Tweets.csv`));
  }

  exportExcel() {
    this.apiService.exportExcel().subscribe(data => {
      //const blob = new Blob([JSON.stringify(data)], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8' });
      saveAs(data, `Tweets.xlsx`)
    });
  }
  /**
  * Busca datos en base a los campos del formulario
  */
  searchDemo() {
    if (this.wordInput == "" || this.wordInput == null || !(this.maxResultsInput > 0)) {
      alert("Todos los campos son obligatorios");
    } else {
      //obtenemos los datos para los chart
      // detengo los charts si es que ya se estaban ejecutando
      this.stopChartsRealTime();
      this.startDataPieChartRealTime();
      this.startDataLineChartRealTime();

      //iniciamos la búsqueda
      this.startDemo();
      //obtenemos los datos para los tweets
      this.startDataTweetsRealTime();
      //actualizo los contadores
      this.startDataCountersRealTime()
      // actualizo la nube de palabras
      this.startDataWordCloudRealTime();
    }
  }
  /**
  * Obtiene los datos para los chart
  */
  startDemo() {
    this.apiService.startDemo(this.wordInput).subscribe(result => {
      this.isSearching = result;
    });
  }

  createImageFromBlob(image: Blob) {
    let reader = new FileReader();
    reader.addEventListener("load", () => {
      this.imageToShow = reader.result;
    }, false);

    if (image) {
      reader.readAsDataURL(image);
    }
  }

  getWordCloud() {
    this.isImageLoading = true;
    this.apiService.getWordCloud().subscribe(data => {
      this.createImageFromBlob(data);
      this.isImageLoading = false;
    }, error => {
      this.isImageLoading = false;
      console.log(error);
    });
  }

  /**
  * Inicia el RealTime para dataPieChart y luego para dataLineChart
  */
  startDataPieChartRealTime() {
    //como la función que quiero enviar al RealTime usa el apiserver debo enviar todo el módulo
    var context = this;
    var functionToExecute = function () {
      context.apiService.getDataForPieChart().subscribe(result => {
        context.dataPieChart = result;
      });
    };

    this.dataPieChartRealTime = new RealTime(3000, functionToExecute);
  }

  startDataLineChartRealTime() {
    //como la función que quiero enviar al RealTime usa el apiserver debo enviar todo el módulo
    var context = this;
    var functionToExecute = function () {
      context.apiService.getDataForLineChart().subscribe(result => {
        context.dataLineChart = result;
      });
    };

    this.dataLineChartRealTime = new RealTime(10000, functionToExecute);
  }

  startDataCountersRealTime() {
    var context = this;
    var functionToExecute = function () {
      context.apiService.getCounters().subscribe(result => {
        context.countAngry = result.data.data.countAggresive;
        context.countNeutral = result.data.data.countNeutral;
        context.countNotAngry = result.data.data.countNonAggresive;
        context.countTotal = result.data.data.countTotal;
      });
    };

    this.dataCountersRealTime = new RealTime(3000, functionToExecute)
  }

  startDataWordCloudRealTime() {
    //como la función que quiero enviar al RealTime usa el apiserver debo enviar todo el módulo
    var context = this;
    var functionToExecute = function () {
      context.apiService.getWordCloud().subscribe(data => {
        context.createImageFromBlob(data);
      });
    };

    this.dataWordCloudRealTime = new RealTime(5000, functionToExecute);

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

  // Detengo todos los gráficos
  stopChartsRealTime() {
    if (this.dataCountersRealTime) {
      this.dataCountersRealTime.stop();
    }
    if (this.dataLineChartRealTime) {
      this.dataLineChartRealTime.stop();
    }
    if (this.dataPieChartRealTime) {
      this.dataPieChartRealTime.stop();
    }
    if (this.dataWordCloudRealTime) {
      this.dataWordCloudRealTime.stop();
    }
  }

}


