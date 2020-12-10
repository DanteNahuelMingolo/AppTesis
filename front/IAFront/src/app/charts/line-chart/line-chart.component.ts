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
  lineChartOptions: any;
  lineChartColors: Color[];
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
        this.lineChartData = [
          {
            data: this.response.data.data,
            label: this.response.data.label
          },
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
      {
        borderColor: 'black',
        backgroundColor: 'rgba(255,255,0,0.28)',
      },
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
