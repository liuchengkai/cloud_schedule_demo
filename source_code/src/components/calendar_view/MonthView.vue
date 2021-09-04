<template>
<div v-if="getDatesDone">
    <el-row class="calendar_row">
        <el-col :xs=24 :sm="9">
            <el-date-picker style="width: 100%"
            v-model="date_selected"
            type="month"
            placeholder="选择月">
            </el-date-picker>
        </el-col>
        <el-col :xs=10 :sm="6">
            <el-button class="block_display" @click="prevMonth">
                上个月
            </el-button>
        </el-col>
        <el-col :xs=4 :sm="3">
            <el-button class="block_display" @click="thisMonth">
                今天
            </el-button>
        </el-col>
        <el-col :xs=10 :sm="6">
            <el-button class="block_display" @click="nextMonth">
                下个月
            </el-button>
        </el-col>
    </el-row>
<el-row class="calendar_row">
    <el-col :span="3" v-for="w in weeks" :key="w" class="week_cell">
        {{w}}
    </el-col>
</el-row>
    <el-row v-for="i in 6" :key="'row'+i" class="calendar_row">
        <el-col :class="dates[(i-1)*7 + (j-1)].type + ' date_cell'" :span="3" v-for="j in 7" :key="'col'+j">
            <span class="date_container"> {{dates[(i-1)*7 + (j-1)].day.getDate()}} </span>
            <template v-if="dates[(i-1)*7 + (j-1)].events.length">
                <time-line v-for="e,  in dates[(i-1)*7 + (j-1)].events" :key="e.title" :tl_color="e.tl_color" :width="e.dur*100 + '%' ">
                    {{e.title}}
                </time-line>
            </template>
        </el-col>
    </el-row>
</div>
</template>

<script>
import axios from 'axios'
import TimeLine from "./TimeLine.vue"
export default {
  name: 'MonthView',
  components: {
      TimeLine,
  },
  
  mounted(){
        axios.get(this.api_path+'/getAll')
        .then(res => {
            for(let e of res.data){
                this.events.push({
                'id': e.idnum,
                'title': e.event,
                'start_date': new Date(e.startTime),
                'end_date': new Date(e.endTime),
                'tl_color': e.color
                })
            }
        this.date_selected = new Date()
        this.today = this.date_selected.getDate()
        this.thisMonth()
        })
  },
  watch: {
      date_selected(newDate) {
        this.cur_year = newDate.getFullYear()
        this.cur_month = newDate.getMonth() + 1
        let temp_date = new Date()
        if(this.cur_year == temp_date.getFullYear() && this.cur_month-1 == temp_date.getMonth()){
            this.today = temp_date.getDate()
        }else{
            this.today = 1
        }
        this.getDatesDone = false
        this.caculate_calendar()
        this.getDatesDone = true
      }
  },
  data() {
    return {
      cur_year: null,
      cur_month: null,
      api_path: 'http://123.57.142.230:5001',
      today: null,
      pic: null,
      weeks: ["日", "一", "二", "三", "四", "五", "六"],
      months: ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"],
      dates: null,
      date_selected: null,
      getDatesDone: false,
      events: []
    }
  },
  methods:{
      // 计算当月的日历
    getAllDates: function(year, month, day){
        let date_arr = []
        let day_of_month = new Date(year.toString()+'/'+month.toString()+'/'+'01')
        let weekday = day_of_month.getDay()
        // 计算当前第一个可见日期（上个月）
        day_of_month.setDate(weekday?-weekday:-7)
        for(let i = 0; i < 42; i++){
            day_of_month.setDate(day_of_month.getDate() + 1)
            let type = null
            let month_temp = day_of_month.getMonth() 
            if(month_temp == month - 2){
                type = 'prevM'
            }else if(month_temp == month - 1){
                if(day_of_month.getFullYear() == this.date_selected.getFullYear() && day_of_month.getMonth() == this.date_selected.getMonth() && day_of_month.getDate() == day){
                    type = 'today'
                }else{
                    type = 'currentM'
                }
            }else{
                type = 'nextM'
            }
            date_arr.push({day: new Date(day_of_month), type: type, events: []})
        }
        return date_arr
    },
    nextMonth: function(){
        this.cur_year = this.cur_month == 12 ? this.cur_year + 1 : this.cur_year
        this.cur_month = this.cur_month == 12 ? 1 : this.cur_month + 1
        this.date_selected = new Date(this.cur_year + '/' + this.cur_month + '/1')
    },
    prevMonth: function(){
        this.cur_year = this.cur_month == 1 ? this.cur_year - 1 : this.cur_year
        this.cur_month = this.cur_month == 1 ? 12 : this.cur_month - 1
        this.date_selected = new Date(this.cur_year + '/' + this.cur_month + '/1')
    },
    thisMonth: function(){
        this.date_selected = new Date()
    },
    getDuration: function(start, end){
        if(start>end){
            return 0
        }
        if(start.getFullYear() == end.getFullYear() && start.getMonth() == end.getMonth() && start.getDate() == end.getDate()){
            return 1
        }else{
            return Math.ceil(end - start)/(1*24*60*60*1000)
        }
    },
    getTimeLine: function(title, dur, tl_color){
        return {'title': title, 'dur': dur, 'tl_color': tl_color}
    },
    // 将日程添加到对应的日历日期上
    addEvents: function(){
        // 存储每行存在的事件数目
        let row_count = [0,0,0,0,0,0]
        // 当前月事件 索引:类型，类型0 - 与当前可见月无关事件，类型1 - 开始日期在当前可见月，类型2 - 不属于类型1但结束日期在当前可见月或未来
        let cur_month_events_index = new Map()
        for(let e_index = 0; e_index < this.events.length; e_index++){
            if(this.dates[0].day <= this.events[e_index].start_date && this.events[e_index].start_date <= this.dates[this.dates.length-1].day){
                cur_month_events_index.set(e_index, 1)
            }else if(this.dates[0].day > this.events[e_index].start_date && !(this.events[e_index].end_date < this.dates[0].day)){
                cur_month_events_index.set(e_index, 2)
            }else{
                cur_month_events_index.set(e_index, 0)
            }
        }
        for(let key of cur_month_events_index.keys()){
            // 如果日程事件的开始日期在这个月，则直接在对应的日期上添加
            let dur = 0, d_i = 0
            if(cur_month_events_index.get(key) == 1){
                dur = this.getDuration(this.events[key].start_date, this.events[key].end_date > this.dates[this.dates.length - 1].day ? this.dates[this.dates.length - 1].day : this.events[key].end_date)
                // 计算日期对应格子的索引
                d_i = this.getDuration(this.dates[0].day, this.events[key].start_date)
            }else if(cur_month_events_index.get(key) == 2){
                dur = this.getDuration(this.dates[0].day, this.events[key].end_date > this.dates[this.dates.length - 1].day ? this.dates[this.dates.length - 1].day : this.events[key].end_date)
                d_i = 0
            }else{
                continue
            }
            let c_row = Math.floor(d_i / 7)
            let c_col = d_i % 7
            let col_available = 7 - c_col
            // 如果当前行非首格已经有添加事件，需要腾出空间
            if(c_col!=0){
                for(let rc = 0; rc<row_count[c_row]; rc++){
                    this.dates[d_i].events.push(this.getTimeLine("", 1, "rgba(0,0,0,0)"))
                }
            }
            // 画当前行
            this.dates[d_i].events.push(this.getTimeLine(this.events[key].title, col_available < dur ? col_available : dur, this.events[key].tl_color))
            row_count[c_row]++
            // 没画完，且不是最后一行继续加
            if(col_available <= dur && c_row != 5){
                let remained = dur - col_available
                let rows_to_add = Math.floor(remained / 7)
                let cols_to_add = remained % 7 + 1
                for(let r = 1; r <= rows_to_add; r++){
                    this.dates[(c_row + r)*7].events.push(this.getTimeLine(this.events[key].title, 7, this.events[key].tl_color))
                    row_count[c_row+r]++
                }
                this.dates[(c_row + rows_to_add + 1) * 7].events.push(this.getTimeLine(this.events[key].title, cols_to_add, this.events[key].tl_color))
                row_count[c_row + rows_to_add + 1]++
            }
            
        }
    },
    caculate_calendar: function(){
        this.dates = this.getAllDates(this.cur_year, this.cur_month, this.today)
        this.addEvents()
    }
  },
}
</script>
<style>
  .is-selected {
    color: #1989FA;
  }
  .calendar_title{
    font-size: 24px
  }
  .block_display{
      width: 100%;
  }
  .today{
      background-color: skyblue;
  }
  .prevM{
      background-color: #BDBDBD;
      color: #757575;
  }
  .nextM{
      background-color: #BDBDBD;
      color: #757575;
  }
  .currentM{
      color: #212121;
  }
  .today{
      background-color: #FFC107;
  }
  .date_cell{
      min-height: 50px;
      border: 1px solid #d8d8d8;
      margin: 0px -1px -1px 0px ;
  }
  .date_container{
      padding: 4px;
  }
  .calendar_row{
      justify-content: center;
  }
  .fake_timeline{
      height: 24px;
  }
  .week_cell{
      margin-top: 8px;
      border-top: 1px solid #d8d8d8;
      text-align: center;
  }
</style>