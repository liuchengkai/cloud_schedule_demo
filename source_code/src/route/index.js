import { createRouter,createWebHashHistory} from "vue-router"

const schedule_edit = () => import("../components/schedule_edit/ScheduleEdit")
const calendar_view = () => import("../components/calendar_view/CalendarView")
const notebook = () => import("../components/notebook/NoteBook")

const routes = [
  { 
    path: "/",
    redirect: "/calendar_view" 
  },
  {
    path: "/schedule_edit",
    name: "schedule_edit",
    component: schedule_edit
  },
  {
    path: "/calendar_view",
    name: "calendar_view",
    component: calendar_view
  },
  {
    path: "/notebook",
    name: "notebook",
    component: notebook
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes: routes
})

export default router
  