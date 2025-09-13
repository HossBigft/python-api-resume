import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { useAuth } from "../__root";
import { useRouter } from "@tanstack/react-router";

export const Route = createFileRoute("/resume/")({
  component: ResumeListPage,
});

type ResumeItem = {
  id: string;
  title: string;
};

function ResumeListPage() {
  const auth = useAuth();
  const router = useRouter();
  const [resumes, setResumes] = useState<ResumeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [newTitle, setNewTitle] = useState("");
  const [newContent, setNewContent] = useState("");
  const [adding, setAdding] = useState(false);
  const [addError, setAddError] = useState<string | null>(null);

  const token = localStorage.getItem("authToken");

  const fetchResumes = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/v1/resume/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (!res.ok) {
        if (res.status === 404) {
          setResumes([]);
          return;
        } else {
          throw new Error("Failed to fetch resumes");
        }
      }
      const data: ResumeItem[] = await res.json();
      setResumes(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!auth.isLoggedIn) {
      router.navigate({ to: "/login" });
      return;
    }
    fetchResumes();
  }, [auth.isLoggedIn, router]);

  const handleAddResume = async (e: React.FormEvent) => {
    e.preventDefault();
    setAdding(true);
    setAddError(null);
    try {
      const res = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/v1/resume/`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ title: newTitle, content: newContent }),
        }
      );
      if (!res.ok) throw new Error("Failed to add resume");
      setNewTitle("");
      setNewContent("");
      await fetchResumes();
    } catch (err: any) {
      setAddError(err.message);
    } finally {
      setAdding(false);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div style={{ padding: 20 }}>
      <h1>Your Resumes</h1>

      {resumes.length === 0 ? (
        <p>There are no resumes.</p>
      ) : (
        <ul>
          {resumes.map((r) => (
            <li key={r.id}>{r.title}</li>
          ))}
        </ul>
      )}

      <h2>Add Resume</h2>
      <form onSubmit={handleAddResume} style={{ marginTop: 10 }}>
        <div>
          <input
            placeholder="Title"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            required
          />
        </div>
        <div>
          <textarea
            placeholder="Content"
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={adding}>
          {adding ? "Adding..." : "Add Resume"}
        </button>
        {addError && <p style={{ color: "red" }}>{addError}</p>}
      </form>
    </div>
  );
}
