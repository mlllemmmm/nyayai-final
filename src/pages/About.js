import React from "react";

function About() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-primary-50/20 to-indigo-50/30">
      <div className="max-w-4xl mx-auto px-4 py-16 md:py-24">
        <h1 className="text-4xl font-bold text-slate-800 text-center mb-12">Who We Are</h1>
        <div className="bg-white rounded-2xl shadow-lg border border-slate-100 p-8 md:p-12 space-y-6 text-slate-600 leading-relaxed">
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
    </div>
  );
}

export default About;
