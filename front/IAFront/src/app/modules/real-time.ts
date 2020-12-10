import { interval, Observable, Subscription } from 'rxjs';

export class RealTime {
  //atributos para funcionalidad
  realTimeInterval: Observable<number>;
  realTimeSession: Subscription;

  /**
  * Configuración y seteo de lo necesario para poder usar el RealTime
  * @param intervalTime en milisegundos
  * @param functionToExecute función que se ejecutará
  */
  constructor(intervalTime: number, functionToExecute: Function) {
    //realizamos la configuración inicial
    this.realTimeInterval = interval(intervalTime);

    //iniciamos la sesion de RealTime
    this.start(functionToExecute);
  }

  /**
  * Detiene la ejecución del RealTime
  */
  stop(){
    this.realTimeSession.unsubscribe();
  }

  /**
  * Inicia la ejecución del RealTime
  * @param functionToExecute función que se ejecutará
  */
  start(functionToExecute: Function){
    //si ya existe una sesion iniciada previamente la destruye
    if(this.realTimeSession){
      this.stop();
    }    

    this.realTimeSession = this.realTimeInterval.subscribe(session => {
        functionToExecute();
    });
  }
}
