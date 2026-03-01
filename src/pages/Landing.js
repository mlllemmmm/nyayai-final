import React, { useEffect } from "react";
import { Link, useLocation } from "react-router-dom";

function Landing() {
  const location = useLocation();

  useEffect(() => {
    const hash = location.hash?.slice(1);
    if (hash) {
      const el = document.getElementById(hash);
      if (el) setTimeout(() => el.scrollIntoView({ behavior: "smooth" }), 100);
    }
  }, [location]);

  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section id="hero" className="relative overflow-hidden bg-gradient-to-br from-slate-50 via-primary-50/30 to-indigo-50/40 pt-12 pb-24 md:pt-20 md:pb-32">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-slate-800 tracking-tight leading-tight">
            Democratizing Legal Knowledge in India using AI
          </h1>
          <p className="mt-6 text-lg sm:text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed">
            NyayaAI uses Retrieval-Augmented Generation (RAG) over 1600+ sections of Indian law to provide accurate, explainable legal guidance.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/assistant"
              className="inline-flex items-center justify-center px-6 py-3.5 rounded-xl bg-gradient-to-r from-primary-700 to-indigo-600 text-white font-semibold shadow-lg hover:shadow-xl hover:opacity-95 transition-all"
            >
              Try Legal Assistant
            </Link>
            <a
              href="#about"
              onClick={(e) => {
                e.preventDefault();
                document.getElementById("about")?.scrollIntoView({ behavior: "smooth" });
              }}
              className="inline-flex items-center justify-center px-6 py-3.5 rounded-xl border-2 border-primary-200 text-primary-700 font-semibold hover:bg-primary-50 transition-colors"
            >
              Learn More
            </a>
          </div>
        </div>
      </section>

      {/* About */}
      <section id="about" className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-slate-800 text-center mb-10">Who We Are</h2>
          <div className="prose prose-slate max-w-none text-slate-600 space-y-4 text-center">
            <p className="text-lg">
              NyayaAI is an AI-powered legal assistant built to make Indian laws accessible to everyone. We believe that understanding your rights and obligations should not require a law degree.
            </p>
            <p>
              Our system uses section-level embeddings from 12 major Indian Acts—covering areas from consumer rights to labour law—so you get precise, traceable answers grounded in the actual text of the law.
            </p>
            <p>
              Whether you are a student, a citizen navigating a dispute, a startup checking compliance, or a researcher exploring Indian legislation, NyayaAI is designed to give you clear, explainable legal guidance at your fingertips.
            </p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 bg-gradient-to-b from-slate-50 to-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-slate-800 text-center mb-14">Features</h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                title: "RAG-Based Legal Assistant",
                desc: "Uses a vector database to retrieve exact relevant law sections and generate answers grounded in statute, reducing hallucinations.",
                icon: "📚",
              },
              {
                title: "Section-Level Precision",
                desc: "1603 embedded sections with metadata including Act and Section number for precise citations.",
                icon: "🎯",
              },
              {
                title: "Voice Input Support",
                desc: "Users can speak their legal queries and get the same accurate guidance via voice.",
                icon: "🎤",
              },
              {
                title: "Multilingual Capability",
                desc: "Legal guidance simplified in plain language for broader accessibility.",
                icon: "🌐",
              },
              {
                title: "Explainable Responses",
                desc: "Every answer shows the legal basis—which sections were used—so you can verify and trust the output.",
                icon: "✓",
              },
            ].map((f) => (
              <div
                key={f.title}
                className="bg-white rounded-xl p-6 shadow-md border border-slate-100 hover:shadow-lg hover:border-primary-100 transition-all duration-200"
              >
                <div className="text-3xl mb-3">{f.icon}</div>
                <h3 className="text-lg font-semibold text-slate-800 mb-2">{f.title}</h3>
                <p className="text-slate-600 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-slate-800 text-center mb-14">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-14 h-14 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center text-xl font-bold mx-auto mb-4">1</div>
              <h3 className="font-semibold text-slate-800 mb-2">Ask your question</h3>
              <p className="text-slate-600 text-sm">Enter your legal question or describe your situation in plain language.</p>
            </div>
            <div className="text-center">
              <div className="w-14 h-14 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center text-xl font-bold mx-auto mb-4">2</div>
              <h3 className="font-semibold text-slate-800 mb-2">Retrieval from law</h3>
              <p className="text-slate-600 text-sm">NyayaAI retrieves the most relevant sections from the vector database.</p>
            </div>
            <div className="text-center">
              <div className="w-14 h-14 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center text-xl font-bold mx-auto mb-4">3</div>
              <h3 className="font-semibold text-slate-800 mb-2">Structured explanation</h3>
              <p className="text-slate-600 text-sm">The AI generates a clear, structured legal explanation with citations.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA strip */}
      <section className="py-16 bg-gradient-to-r from-primary-800 to-indigo-700">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <p className="text-white text-xl font-semibold mb-6">Ready to get legal guidance?</p>
          <Link
            to="/assistant"
            className="inline-flex items-center justify-center px-8 py-3.5 rounded-xl bg-white text-primary-800 font-semibold shadow-lg hover:shadow-xl transition-all"
          >
            Try Legal Assistant
          </Link>
        </div>
      </section>
    </div>
  );
}

export default Landing;
