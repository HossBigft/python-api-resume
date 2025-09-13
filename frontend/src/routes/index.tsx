// src/routes/index.tsx
import { createFileRoute } from "@tanstack/react-router";
import { useAuth } from "./__root";
import { useEffect } from "react";
import { useRouter } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: HomePage,
});

function HomePage() {
  const auth = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!auth.isLoggedIn) {
      router.navigate({ to: "/login" });
    }
  }, [auth.isLoggedIn, router]);

  if (!auth.isLoggedIn) {
    return null;
  }

  return (
    <div>
      <h1>Home</h1>
    </div>
  );
}
