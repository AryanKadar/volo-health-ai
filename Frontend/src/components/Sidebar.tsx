import { MessageSquare } from "lucide-react";
import { motion } from "framer-motion";
import { suggestions } from "@/lib/chatData";

interface SidebarProps {
  onSelect: (q: string) => void;
}

const Sidebar = ({ onSelect }: SidebarProps) => (
  <aside className="hidden md:flex flex-col w-[280px] min-w-[280px] bg-sidebar border-r border-border p-5 pt-20 gap-4">
    <h2 className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-1">Quick Questions</h2>
    <div className="flex flex-col gap-2.5">
      {suggestions.map((q, i) => (
        <motion.button
          key={i}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => onSelect(q)}
          className="text-left text-sm px-3.5 py-3 rounded-lg bg-secondary hover:bg-border text-foreground/90 transition-colors leading-relaxed flex items-start gap-2.5"
        >
          <MessageSquare size={14} className="text-primary mt-0.5 shrink-0" />
          {q}
        </motion.button>
      ))}
    </div>
  </aside>
);

export default Sidebar;
