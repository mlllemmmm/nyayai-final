
import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";

function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  const scrollToSection = (id) => {
    setMobileOpen(false);
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <nav className="sticky top-0 z-50 w-full bg-white/90 backdrop-blur-md border-b border-slate-200/80 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 md:h-18">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 shrink-0" onClick={() => setMobileOpen(false)}>
            <span className="text-xl font-bold bg-gradient-to-r from-primary-800 to-indigo-600 bg-clip-text text-transparent">
              NyayaAI
            </span>
            <span className="hidden sm:inline text-xs text-slate-500 font-normal max-w-[140px]">
              AI-Powered Legal Intelligence for India
            </span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-1">
            <Link
              to="/"
              onClick={(e) => {
                if (location.pathname === "/") {
                  e.preventDefault();
                  scrollToSection("hero");
                }
                setMobileOpen(false);
              }}
              className="px-3 py-2 rounded-lg text-slate-600 hover:text-primary-700 hover:bg-primary-50 text-sm font-medium transition-colors"
            >
              Home
            </Link>
            <Link
              to="/about"
              className="px-3 py-2 rounded-lg text-slate-600 hover:text-primary-700 hover:bg-primary-50 text-sm font-medium transition-colors"
            >
              About
            </Link>
            <Link
              to={location.pathname === "/" ? "#features" : "/#features"}
              onClick={(e) => {
                if (location.pathname === "/") {
                  e.preventDefault();
                  scrollToSection("features");
                }
                setMobileOpen(false);
              }}
              className="px-3 py-2 rounded-lg text-slate-600 hover:text-primary-700 hover:bg-primary-50 text-sm font-medium transition-colors"
            >
              Features
            </Link>
            <Link
              to={location.pathname === "/" ? "#how-it-works" : "/#how-it-works"}
              onClick={(e) => {
                if (location.pathname === "/") {
                  e.preventDefault();
                  scrollToSection("how-it-works");
                }
                setMobileOpen(false);
              }}
              className="px-3 py-2 rounded-lg text-slate-600 hover:text-primary-700 hover:bg-primary-50 text-sm font-medium transition-colors"
            >
              How It Works
            </Link>
            <Link
              to="/login"
              className="px-3 py-2 rounded-lg text-slate-600 hover:text-primary-700 hover:bg-primary-50 text-sm font-medium transition-colors"
            >
              Login
            </Link>
            <Link
              to="/assistant"
              className="ml-2 px-4 py-2 rounded-xl bg-gradient-to-r from-primary-700 to-indigo-600 text-white text-sm font-semibold shadow-md hover:shadow-lg hover:opacity-95 transition-all"
            >
              Try Now
            </Link>
          </div>

          {/* Mobile menu button */}
          <button
            type="button"
            className="md:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle menu"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {mobileOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile menu */}
        {mobileOpen && (
          <div className="md:hidden py-4 border-t border-slate-200 space-y-1">
            <Link to="/" className="block px-4 py-2 rounded-lg text-slate-600 hover:bg-primary-50" onClick={() => setMobileOpen(false)}>Home</Link>
            <Link to="/about" className="block px-4 py-2 rounded-lg text-slate-600 hover:bg-primary-50" onClick={() => setMobileOpen(false)}>About</Link>
            <Link
              to="/#features"
              onClick={(e) => {
                if (location.pathname === "/") {
                  e.preventDefault();
                  scrollToSection("features");
                }
                setMobileOpen(false);
              }}
              className="block px-4 py-2 rounded-lg text-slate-600 hover:bg-primary-50"
            >
              Features
            </Link>
            <Link
              to="/#how-it-works"
              onClick={(e) => {
                if (location.pathname === "/") {
                  e.preventDefault();
                  scrollToSection("how-it-works");
                }
                setMobileOpen(false);
              }}
              className="block px-4 py-2 rounded-lg text-slate-600 hover:bg-primary-50"
            >
              How It Works
            </Link>
            <Link to="/login" className="block px-4 py-2 rounded-lg text-slate-600 hover:bg-primary-50" onClick={() => setMobileOpen(false)}>Login</Link>
            <Link to="/assistant" className="block mx-4 mt-2 py-3 text-center rounded-xl bg-gradient-to-r from-primary-700 to-indigo-600 text-white font-semibold" onClick={() => setMobileOpen(false)}>Try Now</Link>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
