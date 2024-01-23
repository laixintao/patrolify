import * as React from "react";
import * as ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import { FocusStyleManager } from "@blueprintjs/core";
import HomePage from "./homepage/HomePage";
import CheckerDetailPage from "./CheckerDetailPage";
import CheckerLayout from "./CheckerLayout";
import CheckDetailPage from "./CheckDetailPage";
import JobDetailPage from "./jobdetailpage/JobDetailPage";

FocusStyleManager.onlyShowFocusOnTabs();

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <HomePage /> },
      {
        path: "checker",
        element: <CheckerLayout />,
        children: [
          {
            path: ":checkerName/job/:checkId/:jobId",
            element: <JobDetailPage />,
          },
          {
            path: ":checkerName/job/:checkId",
            element: <CheckDetailPage />,
          },
          {
            path: ":checkerName",
            element: <CheckerDetailPage />,
            index: true,
          },
        ],
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
