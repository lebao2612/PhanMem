import Home from "../pages/HomePage";
import Login from "../pages/LoginPage";
import Dashboard from "../pages/DashBoardPage";
import EditVideo from "../pages/EditVideoPage";
import AnalystPage from "../pages/AnalystPage";
import Setting from "../pages/SettingPage";
import LoginGoogleCallbackPage from "../pages/LoginGoogleCallbackPage";


const publicRoutes = [
  { path: "/login", component: Login },
  { path: "/", component: Login },
   { path: "/login/google/callback", component: LoginGoogleCallbackPage },
];
const privateRoutes = [
  { path: "/home", component: Home },
  { path: "/dashboard", component: Dashboard },
  { path: "/edit-video", component: EditVideo },
  { path: "/analyst", component: AnalystPage },
  { path: "/setting", component: Setting },
];
export { publicRoutes, privateRoutes };
