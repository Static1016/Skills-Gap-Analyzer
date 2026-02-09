export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center gap-3">
        {/* Logo */}
        <div className="w-10 h-10 bg-blue-600 text-white font-bold flex items-center justify-center rounded-lg">
          SG
        </div>

        {/* Brand */}
        <div>
          <h1 className="text-lg font-semibold leading-tight">
            Skill Gap Analyzer
          </h1>
          <p className="text-xs text-gray-500">
            Resume-based career insights
          </p>
        </div>
      </div>
    </header>
  );
}
