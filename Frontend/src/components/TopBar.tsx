import { ShieldCheck } from "lucide-react";

const TopBar = () => (
  <header className="fixed top-0 left-0 right-0 z-50 h-14 flex items-center justify-between px-4 md:px-6 bg-card border-b border-border backdrop-blur-sm">
    <div className="flex items-center gap-2.5">
      <ShieldCheck className="text-primary" size={22} />
      <span className="font-semibold text-sm md:text-base tracking-tight">
        Volo Health <span className="text-muted-foreground font-normal">•</span> Hospitalisation AI Assistant
      </span>
    </div>
    <span className="hidden sm:inline-flex items-center px-2.5 py-1 rounded-full bg-secondary text-[11px] font-medium text-primary tracking-wide">
      Agentic AI Internship
    </span>
  </header>
);

export default TopBar;
