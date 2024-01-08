import "./App.css";
import AppNavbar from "./Navbar.jsx";
import { Outlet } from "react-router-dom";

function App() {
  return (
    <div>
      <AppNavbar />

      <Outlet />
    </div>
  );
}

export default App;
