import { createFileRoute, useRouter, useParams } from "@tanstack/react-router";
import { useEffect, useState } from "react";

export const Route = createFileRoute("/resume/$resumeId")({
  component: ResumePage,
});

function ResumePage() {
  const router = useRouter();
  const { resumeId } = useParams({ from: "/resume/$resumeId" });

  const [resume, setResume] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [improved, setImproved] = useState<null | {
    id: string;
    title: string;
    content: string;
  }>(null);

  useEffect(() => {
    if (!resumeId) return;

    const fetchResume = async () => {
      try {
        const token = localStorage.getItem("authToken");
        const res = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/api/v1/resume/${resumeId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        if (!res.ok) {
          setError(
            res.status === 404 ? "Resume not found" : "Failed to fetch resume"
          );
          return;
        }

        const data = await res.json();
        setResume(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchResume();
  }, [resumeId]);

  if (!resumeId) return <div>Waiting for resume id…</div>;
  if (loading) return <div>Loading resume...</div>;
  if (error) return <div style={{ color: "red" }}>{error}</div>;
  if (!resume) return null;

  const handleImprove = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem("authToken");
      const res = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/v1/resume/${resumeId}/improve`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (!res.ok) {
        throw new Error(`Failed: ${res.status}`);
      }

      const data = await res.json();
      setImproved(data);
    } catch (err) {
      console.error("Improve error:", err);
      setImproved(null);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div style={{ padding: 20 }}>
      <h1>{resume.title}</h1>
      <p>{resume.content}</p>
      <button onClick={() => router.navigate({ to: "/resume/" })}>
        Back to list
      </button>
      <button onClick={handleImprove} disabled={loading}>
        {loading ? "Improving..." : "Improve"}
      </button>

      {improved && (
        <div className="mt-4 border p-4 rounded bg-gray-50">
          <h2 className="font-bold text-lg">{improved.title}</h2>
          <p className="whitespace-pre-line">{improved.content}</p>
        </div>
      )}
    </div>
  );
}
