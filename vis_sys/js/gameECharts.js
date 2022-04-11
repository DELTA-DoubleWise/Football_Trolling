import { init } from 'echarts';
var gameStat1 = echarts.init(document.getElementById('gameStat1'))
option = {
    title: {
      text: 'Game stats'
    },
    legend: {
      data: ['Tottenham Spurs', 'Leicester City']
    },
    radar: {
      // shape: 'circle',
      indicator: [
        { name: 'possesion percentage', max: 100 },
        { name: 'Shots', max: 30 },
        { name: 'Shots on Target', max: 20 },
        { name: 'Touches', max: 1000 },
        { name: 'Passes', max: 800 },
        { name: 'Yellow Cards', max: 6 }
      ]
    },
    series: [
      {
        name: 'Tottenham Spurs vs Leicester City',
        type: 'radar',
        data: [
          {
            value: [53, 4, 11, 710, 491, 2],
            name: 'Tottenham Spurs'
          },
          {
            value: [47, 6, 10, 651, 444, 0],
            name: 'Leicester City'
          }
        ]
      }
    ]
  };
gameStat1.setOption(option);