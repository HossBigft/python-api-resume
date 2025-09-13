import { Outlet, createRootRoute } from '@tanstack/react-router'
import { TanStackRouterDevtoolsPanel } from '@tanstack/react-router-devtools'
import { TanstackDevtools } from '@tanstack/react-devtools'
import { useState, createContext, useContext } from 'react'


const AuthContext = createContext<{
  isLoggedIn: boolean
  login: () => void
  logout: () => void
} | null>(null)

export const useAuth = () => {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('AuthContext not found')
  return ctx
}

export const Route = createRootRoute({
  component: () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false)
    return (
      <AuthContext.Provider
        value={{
          isLoggedIn,
          login: () => setIsLoggedIn(true),
          logout: () => setIsLoggedIn(false),
        }}
      >
        <Outlet />
        <TanstackDevtools
          config={{ position: 'bottom-left' }}
          plugins={[
            {
              name: 'Tanstack Router',
              render: <TanStackRouterDevtoolsPanel />,
            },
          ]}
        />
      </AuthContext.Provider>
    )
  },
})
