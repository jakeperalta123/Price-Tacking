import UserRegister from "./pages/Register";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import LandingPage from "./pages/LandingPage";
import { BrowserRouter, Routes, Route} from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<UserRegister />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/" element={<LandingPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;