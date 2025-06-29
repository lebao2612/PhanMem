import Home from "../pages/HomePage";
import Login from "../pages/LoginPage";
import Register from "../pages/RegisterPage";
import Dashboard from "../pages/DashBoardPage";
import EditVideo from "../pages/EditVideoPage";

const publicRoutes = [
  { path: "/login", component: Login },
  { path: "/register", component: Register },
];
const privateRoutes = [
  { path: "/home", component: Home },
  { path: "/dashboard", component: Dashboard },
  { path: "/edit-video", component: EditVideo },
];
export { publicRoutes, privateRoutes };
