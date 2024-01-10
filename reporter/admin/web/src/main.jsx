import * as React from "react";
import * as ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import { FocusStyleManager } from "@blueprintjs/core";
import HomePage from "./HomePage";
import CheckerDetailPage from "./CheckerDetailPage";

FocusStyleManager.onlyShowFocusOnTabs();

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <HomePage />},
      {
        path: "checker/:checkerName",
        element: <CheckerDetailPage />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
