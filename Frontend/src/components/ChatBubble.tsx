import { motion } from "framer-motion";
import { ShieldCheck } from "lucide-react";
import type { Message } from "@/lib/chatData";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const ChatBubble = ({ role, content }: Message) => {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-2.5 max-w-[85%] ${isUser ? "ml-auto flex-row-reverse" : ""}`}
    >
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-primary/15 flex items-center justify-center shrink-0 mt-1">
          <ShieldCheck size={16} className="text-primary" />
        </div>
      )}
      <div
        className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${isUser
          ? "bg-chat-user text-primary-foreground rounded-tr-md"
          : "bg-chat-assistant text-foreground rounded-tl-md prose prose-sm prose-invert max-w-none prose-p:leading-relaxed prose-pre:bg-secondary prose-pre:text-secondary-foreground prose-strong:text-white prose-li:text-gray-200"
          }`}
      >
        {isUser ? (
          content
        ) : (
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
        )}
      </div>
    </motion.div>
  );
};

export default ChatBubble;
