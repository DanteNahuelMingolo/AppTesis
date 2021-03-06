import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Pipe, PipeTransform } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { ChartsModule } from 'ng2-charts';

import { PieChartComponent } from './charts/pie-chart/pie-chart.component';
import { LineChartComponent } from './charts/line-chart/line-chart.component';
import { HomeComponent } from './home/home.component';

import { ApiService } from './api.service';
import { HttpClientModule } from "@angular/common/http";
import { TweetListComponent } from './tweet-list/tweet-list.component';
import { SearchComponent } from './search/search.component';
import { TruncatePipe } from './truncate.pipe';
import { WordcloudComponent } from './wordcloud/wordcloud.component';
import { DemoComponent } from './demo/demo.component';

@NgModule({
  declarations: [
    AppComponent,
    PieChartComponent,
    LineChartComponent,
    HomeComponent,
    TweetListComponent,
    SearchComponent,
    TruncatePipe,
    WordcloudComponent,
    DemoComponent,
  ],
  imports: [
    HttpClientModule,
    FormsModule,
    BrowserModule,
    AppRoutingModule,
    ChartsModule
  ],
  providers: [
    ApiService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
