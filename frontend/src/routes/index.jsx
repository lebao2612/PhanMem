import Home from "../pages/HomePage";
import Login from "../pages/LoginPage";
import Register from "../pages/RegisterPage";
import Dashboard from "../pages/DashBoardPage";
import TestReview from "../pages/TestReviewPage";

const publicRoutes = [
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/review", component: TestReview },
];
const privateRoutes = [
  { path: "/home", component: Home },
  { path: "/dashboard", component: Dashboard },
];

export { publicRoutes, privateRoutes };
