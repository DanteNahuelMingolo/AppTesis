import { Component, Input, OnInit } from '@angular/core';
import { ChartType, ChartOptions } from 'chart.js';
import { SingleDataSet, Label, Color, monkeyPatchChartJsLegend, monkeyPatchChartJsTooltip } from 'ng2-charts';
import * as pluginLabels from 'chartjs-plugin-labels';
import { ObjectUnsubscribedError } from 'rxjs';

@Component({
  selector: 'app-pie-chart',
  templateUrl: './pie-chart.component.html',
  styleUrls: ['./pie-chart.component.css']
})
export class PieChartComponent implements OnInit {
  //data recibida del componente padre
  @Input()
  response: any;

  //atributos necesarios para el chart
  public pieChartOptions: ChartOptions;
  public pieChartLabels: Label[] = [];
  public pieChartData: SingleDataSet = [];
  public pieChartType: ChartType;
  public pieChartLegend: boolean;
  public pieChartPlugins: any[];

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
      if(this.response.data.data){
        this.pieChartData = this.response.data.data;
        this.pieChartLabels = this.response.data.chartLabels;
        this.pieChartPlugins = [pluginLabels]
        //si hay data el dataLoaded debe estar en true
        this.setDataLoaded(true);
      }
    }else{
      //si no hay data el dataLoaded debe estar en false
      this.setDataLoaded(false);
    }
  }

  /**
  * Configuración inicial
  */
  initialConfiguration(){
    this.pieChartOptions = {
      responsive: true,
      plugins: {
        labels: {
          render: 'percentage',
          arc:false,
          position:'outside',
          textShadow:false,
          fontStyle:'normal',
          fontFamily: "Lato",
          fontSize: 20,
          fontColor: ['#6c757d', '#6c757d', '#6c757d'],
          precision: 2
        }
    },
  }

    this.pieChartType = 'pie';
    this.pieChartLegend = true;
    this.pieChartPlugins = [];

    //iniciamos así los datos y labels porque el chart tiene un bug para el pie
    //y no muestra colores si inicialmente no está cargado 
    this.pieChartData = [0,0,0];
    this.pieChartLabels = ["","",""];

    monkeyPatchChartJsTooltip();
    monkeyPatchChartJsLegend();
  }

  /**
  * Establece si se deberá mostrar el Chart o no
  * @param loaded verdader o falso
  */
  setDataLoaded(loaded: boolean){
    this.dataLoaded = loaded;
  }
}
