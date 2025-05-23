import Home from "../pages/HomePage";
import Login from "../pages/LoginPage";
import Register from "../pages/RegisterPage";

const publicRoutes = [
  { path: "/login", component: Login },
  { path: "/register", component: Register },
];
const privateRoutes = [{ path: "/home", component: Home }];

export { publicRoutes, privateRoutes };
