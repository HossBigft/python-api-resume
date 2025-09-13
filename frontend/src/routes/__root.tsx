import { Outlet, createRootRoute } from "@tanstack/react-router";
import { TanStackRouterDevtoolsPanel } from "@tanstack/react-router-devtools";
import { TanstackDevtools } from "@tanstack/react-devtools";
import { useState, createContext, useContext, useEffect } from "react";

type AuthType = {
  isLoggedIn: boolean;
  login: () => void;
  logout: () => void;
};

const AuthContext = createContext<AuthType | null>(null);
export const Route = createRootRoute({
  component: RootLayout,
});

function RootLayout() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("authToken");
    if (token) setIsLoggedIn(true);
  }, []);

  const auth: AuthType = {
    isLoggedIn,
    login: () => setIsLoggedIn(true),
    logout: () => {
      setIsLoggedIn(false);
      localStorage.removeItem("authToken");
    },
  };

  return (
    <AuthContext.Provider value={auth}>
      <Outlet />
      <TanstackDevtools
        config={{ position: "bottom-left" }}
        plugins={[
          { name: "Tanstack Router", render: <TanStackRouterDevtoolsPanel /> },
        ]}
      />
    </AuthContext.Provider>
  );
}
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("AuthContext missing");
  return ctx;
}
