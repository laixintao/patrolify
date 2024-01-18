import "./App.css";
import AppNavbar from "./Navbar.jsx";
import { Outlet } from "react-router-dom";

function App() {
  return (
    <div>
      <AppNavbar />

      <div className="app-body">
        <Outlet />
      </div>
    </div>
  );
}

export default App;
