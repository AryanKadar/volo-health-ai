import { MessageSquare } from "lucide-react";
import { suggestions } from "@/lib/chatData";

interface Props {
  onSelect: (q: string) => void;
}

const MobileSuggestions = ({ onSelect }: Props) => (
  <div className="md:hidden flex gap-2 overflow-x-auto px-4 py-3 border-b border-border scrollbar-thin">
    {suggestions.map((q, i) => (
      <button
        key={i}
        onClick={() => onSelect(q)}
        className="shrink-0 flex items-center gap-1.5 text-xs px-3 py-2 rounded-full bg-secondary text-foreground/80 hover:bg-border transition-colors"
      >
        <MessageSquare size={12} className="text-primary" />
        <span className="max-w-[180px] truncate">{q}</span>
      </button>
    ))}
  </div>
);

export default MobileSuggestions;
