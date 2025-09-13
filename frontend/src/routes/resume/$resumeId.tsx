import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { useAuth } from "../__root";
import { useRouter } from "@tanstack/react-router";

export const Route = createFileRoute("/resume/$resumeId")({
  component: ResumeDetailPage,
});

type Resume = {
  id: string;
  title: string;
  content: string;
};

function ResumeDetailPage() {
  const auth = useAuth();
  const router = useRouter();
  const [resume, setResume] = useState<Resume | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const resumeId = router.params.resumeId as string;

  useEffect(() => {
    if (!auth.isLoggedIn) {
      router.navigate({ to: "/login" });
      return;
    }

    const fetchResume = async () => {
      try {
        const token = localStorage.getItem("authToken");
        if (!token) throw new Error("No token found");

        const res = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/api/v1/resume/${resumeId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        if (!res.ok) {
          if (res.status === 404) {
            setResume(null);
            return;
          } else {
            throw new Error("Failed to fetch resume");
          }
        }

        const data: Resume = await res.json();
        setResume(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchResume();
  }, [auth.isLoggedIn, resumeId, router]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!resume) return <p>Resume not found.</p>;

  return (
    <div style={{ padding: 20 }}>
      <h1>{resume.title}</h1>
      <p>{resume.content}</p>
    </div>
  );
}
