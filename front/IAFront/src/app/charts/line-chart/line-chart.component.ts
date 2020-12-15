import { Component, OnInit, Input } from '@angular/core';
import { ChartDataSets } from 'chart.js';
import { Color, Label } from 'ng2-charts';

@Component({
  selector: 'app-line-chart',
  templateUrl: './line-chart.component.html',
  styleUrls: ['./line-chart.component.css']
})
export class LineChartComponent implements OnInit {
  //data recibida del componente padre
  @Input()
  response: any;

  //atributos necesarios para el chart
  lineChartData: ChartDataSets[] = [];
  lineChartLabels: Label[] = [];
  lineChartColors: Color[] = []
  lineChartOptions: any;
  lineChartLegend: boolean;
  lineChartPlugins: any[];
  lineChartType: string;


  //atributo para indicar si se debe mostrar el chart
  //o el mensaje de que no se cargó data aún
  dataLoaded: boolean;

  /**
  * Configuración y seteo de lo necesario para el Chart
  */
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
    if(this.response){
      if(this.response.data){
        this.lineChartData=[
          {data: this.response.data.data[0].values, label: this.response.data.data[0].lineLabel},
          {data: this.response.data.data[1].values, label: this.response.data.data[1].lineLabel},
          {data: this.response.data.data[2].values, label: this.response.data.data[2].lineLabel}
        ];
  
        this.lineChartLabels = this.response.data.chartLabels;

        //si hay data el dataLoaded debe estar en true
        this.setDataLoaded(true);
      }else{
        //si no hay data el dataLoaded debe estar en false
        this.setDataLoaded(false);
      }
    }
  }

  /**
  * Configuración inicial
  */
  initialConfiguration(){
    this.lineChartOptions = {
      responsive: true,
    };

    this.lineChartColors = [
      { // No agresivo
        backgroundColor: 'rgba(148,159,177,0.0)',
        borderColor: '#86c7f3',
        pointBackgroundColor: 'rgba(148,159,177,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(148,159,177,0.8)'
      },
      { // Agresivo
        backgroundColor: 'rgba(77,83,96,0.0)',
        borderColor: '#ffa1b5',
        pointBackgroundColor: 'rgba(77,83,96,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(77,83,96,1)'
      },
      { // Neutro
        backgroundColor: 'rgba(255,0,0,0.0)',
        borderColor: '#ffe29a',
        pointBackgroundColor: 'rgba(148,159,177,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(148,159,177,0.8)'
      }
    ];

    this.lineChartLegend = true;
    this.lineChartPlugins = [];
    this.lineChartType = 'line';
  }

  /**
  * Establece si se deberá mostrar el Chart o no
  * @param loaded verdader o falso
  */
  setDataLoaded(loaded: boolean){
    this.dataLoaded = loaded;
  }
}
