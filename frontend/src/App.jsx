import "./App.css";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { AuthProvider } from "./contexts/AuthContext";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import { publicRoutes, privateRoutes } from "./routes";

const clientId =
  "921617590005-bo9iapdh1iv5ukcut56mk21j7orsihpr.apps.googleusercontent.com";

function App() {
  // const [count, setCount] = useState(0);

  return (
    <>
      <GoogleOAuthProvider clientId={clientId}>
        <AuthProvider>
          <Router>
            <Routes>
              {publicRoutes.map((route, index) => {
                const Page = route.component;
                return (
                  <Route key={index} path={route.path} element={<Page />} />
                );
              })}
              {privateRoutes.map((route, index) => {
                const Page = route.component;
                return (
                  <Route
                    key={index}
                    path={route.path}
                    element={
                      <ProtectedRoute>
                        <Page />
                      </ProtectedRoute>
                    }
                  />
                );
              })}
            </Routes>
          </Router>
        </AuthProvider>
      </GoogleOAuthProvider>
    </>
  );
}

export default App;
