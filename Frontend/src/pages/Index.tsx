import { useState, useRef, useEffect, useCallback } from "react";
import TopBar from "@/components/TopBar";
import Sidebar from "@/components/Sidebar";
import MobileSuggestions from "@/components/MobileSuggestions";
import ChatBubble from "@/components/ChatBubble";
import TypingIndicator from "@/components/TypingIndicator";
import ChatInput from "@/components/ChatInput";
import { Message } from "@/lib/chatData";
import { sendChat, ChatMessage } from "@/lib/api";
import { motion } from "framer-motion";
import { ShieldCheck } from "lucide-react";

const Index = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [history, setHistory] = useState<ChatMessage[]>([]); // last 6 turns
  const [summary, setSummary] = useState<string>("");
  const [typing, setTyping] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, typing]);

  const handleSend = useCallback(
    async (text: string) => {
      // 1. Add user message to UI immediately
      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), role: "user", content: text },
      ]);
      setTyping(true);

      try {
        // 2. Send to backend
        const response = await sendChat(text, history, summary);

        // 3. Add AI reply to UI
        setMessages((prev) => [
          ...prev,
          { id: crypto.randomUUID(), role: "assistant", content: response.reply },
        ]);

        // 4. If on topic, update the history array (keep last 6) and summary
        if (response.on_topic) {
          setHistory((prev) => {
            const newHistory = [
              ...prev,
              { role: "user", content: text },
              { role: "assistant", content: response.reply }
            ] as ChatMessage[];

            // Keep only the last 6 turns (3 Qs, 3 As max)
            return newHistory.slice(-6);
          });

          if (response.new_summary) {
            setSummary(response.new_summary);
          }
        }

      } catch (error: any) {
        console.error("Chat error:", error);
        setMessages((prev) => [
          ...prev,
          {
            id: crypto.randomUUID(),
            role: "assistant",
            content: `Error: ${error.message || "Failed to connect to the backend."}`
          },
        ]);
      } finally {
        setTyping(false);
      }
    },
    [history, summary]
  );

  return (
    <div className="h-screen flex flex-col bg-background">
      <TopBar />
      <div className="flex flex-1 pt-14 overflow-hidden">
        <Sidebar onSelect={handleSend} />
        <main className="flex-1 flex flex-col min-w-0">
          <MobileSuggestions onSelect={handleSend} />
          <div className="flex-1 overflow-y-auto px-4 md:px-6 py-6 scrollbar-thin">
            <div className="max-w-3xl mx-auto flex flex-col gap-4">
              {messages.length === 0 && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex flex-col items-center justify-center h-[50vh] text-center gap-3"
                >
                  <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center">
                    <ShieldCheck size={28} className="text-primary" />
                  </div>
                  <h2 className="text-lg font-semibold">How can I help you today?</h2>
                  <p className="text-sm text-muted-foreground max-w-sm">
                    Ask me anything about hospital admissions, surgery preparation, discharge, or follow-up care.
                  </p>
                </motion.div>
              )}
              {messages.map((msg) => (
                <ChatBubble key={msg.id} {...msg} />
              ))}
              {typing && <TypingIndicator />}
              <div ref={bottomRef} />
            </div>
          </div>
          <ChatInput onSend={handleSend} disabled={typing} />
          <p className="text-center text-[11px] text-muted-foreground py-2">
            Demo for Volo Health Agentic AI Internship
          </p>
        </main>
      </div>
    </div>
  );
};

export default Index;
