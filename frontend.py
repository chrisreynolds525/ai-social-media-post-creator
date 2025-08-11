import React, { useState } from "react";
import "./styles.css";
import { motion } from "framer-motion";
import { Copy, Download, Calendar } from "lucide-react";

function PlatformBadge({ platform }) {
  const colors = {
    twitter: "bg-sky-100 text-sky-800",
    instagram: "bg-pink-100 text-pink-800",
    linkedin: "bg-blue-100 text-blue-800",
    facebook: "bg-indigo-100 text-indigo-800",
  };
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${colors[platform] || 'bg-gray-100 text-gray-800'}`}>
      {platform.charAt(0).toUpperCase() + platform.slice(1)}
    </span>
  );
}

export default function App() {
  const [topic, setTopic] = useState("");
  const [platform, setPlatform] = useState("twitter");
  const [tone, setTone] = useState("engaging");
  const [count, setCount] = useState(3);
  const [loading, setLoading] = useState(false);
  const [posts, setPosts] = useState([]);
  const [scheduledAt, setScheduledAt] = useState("");

  async function generate() {
    if (!topic.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, platform, tone, count }),
      });
      const data = await res.json();
      setPosts(data.posts || []);
    } catch (e) {
      console.error(e);
      alert("Generation failed. Check console.");
    } finally {
      setLoading(false);
    }
  }

  function copyToClipboard(text) {
    navigator.clipboard.writeText(text);
  }

  function downloadCSV() {
    const header = ["platform", "tone", "text", "scheduled_at"];
    const rows = posts.map((p) => [
      platform,
      tone,
      p.text.replace(/\r?\n/g, " "),
      scheduledAt || "",
    ]);
    const csv = [header, ...rows]
      .map((r) => r.map((v) => `"${String(v).replace(/"/g, '""')}"`).join(","))
      .join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `social_posts_${Date.now()}.csv`;
    link.click();
  }

  return (
    <div className="min-h-screen bg-gradient-to-tr from-gray-50 to-white py-12 px-6">
      <div className="max-w-5xl mx-auto">
        <header className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight">AI Social Post Creator</h1>
            <p className="text-gray-500 mt-1">Generate platform-optimized posts with brand voice & hashtag suggestions.</p>
          </div>
        </header>

        <motion.div layout className="bg-white rounded-2xl shadow-lg p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700">Topic or Brief</label>
              <textarea
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                rows={4}
                className="mt-2 block w-full rounded-lg border-gray-200 shadow-sm p-3"
                placeholder="Write a short brief: e.g. 'New eco-friendly shoe launch, emphasizing comfort and sustainability'"
              />

              <div className="mt-4 flex gap-3">
                <div>
                  <label className="text-sm font-medium text-gray-700">Platform</label>
                  <select
                    value={platform}
                    onChange={(e) => setPlatform(e.target.value)}
                    className="mt-2 p-2 rounded-lg border-gray-200"
                  >
                    <option value="twitter">Twitter / X</option>
                    <option value="instagram">Instagram</option>
                    <option value="linkedin">LinkedIn</option>
                    <option value="facebook">Facebook</option>
                  </select>
                </div>

                <div>
                  <label className="text-sm font-medium text-gray-700">Tone</label>
                  <select
                    value={tone}
                    onChange={(e) => setTone(e.target.value)}
                    className="mt-2 p-2 rounded-lg border-gray-200"
                  >
                    <option value="engaging">Engaging</option>
                    <option value="professional">Professional</option>
                    <option value="funny">Playful</option>
                    <option value="inspirational">Inspirational</option>
                  </select>
                </div>

                <div>
                  <label className="text-sm font-medium text-gray-700">Count</label>
                  <input
                    type="number"
                    min={1}
                    max={10}
                    value={count}
                    onChange={(e) => setCount(Number(e.target.value))}
                    className="mt-2 p-2 rounded-lg border-gray-200 w-24"
                  />
                </div>
              </div>

              <div className="mt-4 flex gap-3">
                <button
                  onClick={generate}
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-500 text-white font-semibold shadow hover:bg-emerald-600"
                  disabled={loading}
                >
                  {loading ? "Generating..." : "Generate Posts"}
                </button>

                <div className="flex items-center gap-2">
                  <Calendar size={16} />
                  <input
                    type="datetime-local"
                    value={scheduledAt}
                    onChange={(e) => setScheduledAt(e.target.value)}
                    className="p-2 rounded-lg border-gray-200"
                  />
                </div>

                <button
                  onClick={downloadCSV}
                  className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-100 hover:bg-gray-200"
                >
                  <Download size={16} /> Export CSV
                </button>

                <button
                  onClick={() => {
                    setTopic("");
                    setPosts([]);
                  }}
                  className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-red-50 text-red-700"
                >
                  Clear
                </button>
              </div>
            </div>

            <aside className="p-4 bg-gray-50 rounded-lg">
              <h3 className="text-sm font-semibold text-gray-700">Tips</h3>
              <ul className="mt-2 text-sm text-gray-600 space-y-2">
                <li>Be specific with product details (benefits, audience, CTA).</li>
                <li>Adjust tone to match brand voice.</li>
                <li>Use the CSV export to schedule posts in your social tool.</li>
              </ul>

              <div className="mt-4">
                <h4 className="text-xs uppercase text-gray-400">Template</h4>
                <p className="mt-2 text-sm text-gray-600">"Hook -> Benefit -> CTA + 3 relevant hashtags"</p>
              </div>
            </aside>
          </div>
        </motion.div>

        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Generated Posts</h2>
            <div className="flex items-center gap-2">
              <button onClick={() => setPosts([])} className="px-3 py-1 bg-white rounded-lg shadow">
                Clear
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {posts.length === 0 && (
              <div className="col-span-full p-8 text-center border-2 border-dashed rounded-lg text-gray-400">
                No posts yet — generate something awesome.
              </div>
            )}

            {posts.map((p, i) => (
              <motion.article
                key={i}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white p-4 rounded-xl shadow hover:shadow-lg"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <PlatformBadge platform={platform} />
                    <div>
                      <h3 className="font-semibold">Post Option {i + 1}</h3>
                      <p className="text-xs text-gray-400">
                        Tone: {tone} • Length: {Math.min(280, p.text.length)} chars
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => {
                        copyToClipboard(p.text);
                      }}
                      className="p-2 rounded-md bg-gray-50 hover:bg-gray-100"
                    >
                      <Copy size={14} />
                    </button>
                    <button
                      onClick={() => {
                        setPosts((prev) => prev.filter((_, idx) => idx !== i));
                      }}
                      className="p-2 rounded-md bg-red-50 text-red-600"
                    >
                      Delete
                    </button>
                  </div>
                </div>

                <p className="mt-3 text-gray-800 whitespace-pre-wrap">{p.text}</p>

                <div className="mt-3 flex items-center justify-between text-sm text-gray-500">
                  <div>Hashtags: {p.hashtags?.join(" ")}</div>
                  <div>Schedule: {scheduledAt || "Not set"}</div>
                </div>
              </motion.article>
            ))}
          </div>
        </section>

        <footer className="mt-12 text-center text-sm text-gray-400">
          Built with ❤️ — AI generation powered by your chosen LLM API.
        </footer>
      </div>
    </div>
  );
}
