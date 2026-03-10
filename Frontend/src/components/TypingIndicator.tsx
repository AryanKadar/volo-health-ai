import { ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";

const TypingIndicator = () => (
  <motion.div
    initial={{ opacity: 0, y: 8 }}
    animate={{ opacity: 1, y: 0 }}
    className="flex gap-2.5"
  >
    <div className="w-8 h-8 rounded-full bg-primary/15 flex items-center justify-center shrink-0">
      <ShieldCheck size={16} className="text-primary" />
    </div>
    <div className="bg-chat-assistant px-4 py-3 rounded-2xl rounded-tl-md flex items-center gap-1.5">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="w-2 h-2 rounded-full bg-muted-foreground"
          style={{
            animation: `typing-dot 1.2s ease-in-out ${i * 0.2}s infinite`,
          }}
        />
      ))}
    </div>
  </motion.div>
);

export default TypingIndicator;
