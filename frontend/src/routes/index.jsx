import Home from "../pages/HomePage";
import Login from "../pages/LoginPage";
import Dashboard from "../pages/DashBoardPage";
import EditVideo from "../pages/EditVideoPage";

// import TestReview from "../pages/TestReviewPage";
// import GoogleOAuthCallbackPage from "../pages/GoogleOAuthCallbackPage";

const publicRoutes = [
  { path: "/login", component: Login },
  // { path: "/review", component: TestReview },
  // { path: "/login/google/oauth/callback", component: GoogleOAuthCallbackPage },
];
const privateRoutes = [
  { path: "/home", component: Home },
  { path: "/dashboard", component: Dashboard },
  { path: "/edit-video", component: EditVideo },
];
export { publicRoutes, privateRoutes };
