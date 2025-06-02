import Home from "../pages/HomePage";
import Login from "../pages/LoginPage";
import Register from "../pages/RegisterPage";
import Dashboard from "../pages/DashBoardPage";

const publicRoutes = [
  { path: "/login", component: Login },
  { path: "/register", component: Register },
];
const privateRoutes = [
  { path: "/home", component: Home },
  { path: "/dashboard", component: Dashboard},
];

export { publicRoutes, privateRoutes };
