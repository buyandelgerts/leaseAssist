import { useEffect, useRef, useState } from "react";
import {
  FileText,
  MessageCircle,
  Percent,
  Plus,
  Search,
  Send,
  Settings,
  X,
} from "lucide-react";

type ChatbotOverlayRoute =
  | "home"
  | "search"
  | "detail"
  | "analysis-upload"
  | "analysis-result"
  | "calculator";

interface SessionContext {
  eligibility_result?: string;
  lease_analysis?: string;
}

interface ChatbotOverlayProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  setCurrentView: (view: ChatbotOverlayRoute) => void;
  sessionContext?: SessionContext;
}

interface Message {
  id: string;
  role: "user" | "assistant";
  text: string;
  timestamp: Date;
}

const QUICK_PROMPTS = [
  { label: "Find apartments in Austin under $2000", icon: <Search size={14} /> },
  { label: "Is a 3-month security deposit legal in California?", icon: <FileText size={14} /> },
  { label: "Summarize my eligibility results", icon: <Percent size={14} /> },
  { label: "Walk me through my lease red flags", icon: <MessageCircle size={14} /> },
];

const AI_SERVICE_URL = "http://localhost:8000";

const ChatbotOverlay = ({
  isOpen,
  setIsOpen,
  setCurrentView,
  sessionContext,
}: ChatbotOverlayProps) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      text: "Hello! I'm Assist AI. I can help you find apartments, analyze lease clauses, check your eligibility results, or walk you through red flags. How can I help?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const formatTime = (date: Date) =>
    date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return;

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      text: text.trim(),
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    const history = messages
      .filter((m) => m.id !== "welcome")
      .map((m) => `${m.role === "user" ? "user" : "assistant"}: ${m.text}`);

    try {
      const res = await fetch(`${AI_SERVICE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_question: text.trim(),
          tenant_name: "Tenant",
          conversation_history: history,
          session_context: sessionContext ?? {},
        }),
      });

      if (!res.ok) throw new Error(`Server error ${res.status}`);
      const data = await res.json();
      const reply = data?.result ?? "Sorry, I couldn't get a response.";

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: reply,
          timestamp: new Date(),
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: "I'm having trouble connecting to the server. Please make sure the AI service is running.",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 md:inset-auto md:bottom-6 md:right-6 md:w-150 z-50 flex flex-col bg-white md:rounded-2xl shadow-2xl border border-slate-200 h-full md:h-[80vh] max-h-200 overflow-hidden animate-in slide-in-from-bottom-10 fade-in duration-300">

      {/* Header */}
      <div className="bg-white border-b border-slate-100 p-4 flex justify-between items-center shrink-0">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white">
              <MessageCircle size={20} />
            </div>
            <div className="absolute -bottom-1 -right-1 w-3.5 h-3.5 bg-green-500 border-2 border-white rounded-full" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900 leading-tight">Assist AI</h3>
            <p className="text-xs text-slate-500 flex items-center gap-1">
              <span className="w-1.5 h-1.5 bg-green-500 rounded-full inline-block" />
              Online & Ready to Assist
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            title="settings"
            className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <Settings size={20} />
          </button>
          <button
            title="close"
            onClick={() => setIsOpen(false)}
            className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <X size={20} />
          </button>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-6 bg-slate-50/50 space-y-6">
        <div className="flex justify-center">
          <span className="text-[10px] font-bold text-slate-400 bg-slate-100 px-3 py-1 rounded-full uppercase tracking-wider">
            Today
          </span>
        </div>

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-4 ${msg.role === "user" ? "flex-row-reverse" : ""}`}
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                msg.role === "assistant"
                  ? "bg-slate-200"
                  : "bg-blue-100"
              }`}
            >
              <MessageCircle
                size={14}
                className={msg.role === "assistant" ? "text-slate-500" : "text-blue-600"}
              />
            </div>
            <div className={`flex-1 ${msg.role === "user" ? "flex flex-col items-end" : ""}`}>
              <div
                className={`rounded-2xl p-4 text-sm shadow-sm max-w-[85%] whitespace-pre-wrap ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white rounded-tr-sm"
                    : "bg-white border border-slate-200 text-slate-700 rounded-tl-sm"
                }`}
              >
                {msg.text}
              </div>
              <span className="text-[10px] text-slate-400 mt-1 block px-1">
                {formatTime(msg.timestamp)}
              </span>
            </div>
          </div>
        ))}

        {/* Typing indicator */}
        {loading && (
          <div className="flex gap-4">
            <div className="w-8 h-8 bg-slate-200 rounded-full flex items-center justify-center shrink-0">
              <MessageCircle size={14} className="text-slate-500" />
            </div>
            <div className="bg-white border border-slate-200 rounded-2xl rounded-tl-sm px-5 py-4 shadow-sm">
              <div className="flex gap-1 items-center h-4">
                <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:0ms]" />
                <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:150ms]" />
                <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:300ms]" />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-slate-100 p-4 shrink-0">

        {/* Quick Suggestions */}
        <div className="flex gap-2 overflow-x-auto pb-4 no-scrollbar">
          {QUICK_PROMPTS.map((p) => (
            <button
              key={p.label}
              onClick={() => sendMessage(p.label)}
              disabled={loading}
              className="shrink-0 flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-full text-xs font-semibold text-blue-700 hover:bg-blue-50 transition-colors disabled:opacity-50"
            >
              {p.icon}
              {p.label}
            </button>
          ))}
          <button
            onClick={() => { setIsOpen(false); setCurrentView("calculator"); }}
            className="shrink-0 flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-full text-xs font-semibold text-blue-700 hover:bg-blue-50 transition-colors"
          >
            <Percent size={14} /> Check Eligibility
          </button>
          <button
            onClick={() => { setIsOpen(false); setCurrentView("analysis-upload"); }}
            className="shrink-0 flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-full text-xs font-semibold text-blue-700 hover:bg-blue-50 transition-colors"
          >
            <FileText size={14} /> Analyze Lease
          </button>
        </div>

        <div className="bg-slate-100 rounded-xl p-2 flex items-center gap-2">
          <button
            title="attach"
            className="p-2 text-slate-500 hover:text-slate-800 hover:bg-slate-200 rounded-lg transition-colors"
          >
            <Plus size={20} />
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about leases, properties, or tenant rights..."
            className="flex-1 bg-transparent border-none outline-none text-sm text-slate-700 px-2 placeholder-slate-400"
            disabled={loading}
          />
          <button
            title="send"
            onClick={() => sendMessage(input)}
            disabled={loading || !input.trim()}
            className="w-10 h-10 bg-blue-600 text-white rounded-lg flex items-center justify-center hover:bg-blue-700 transition-colors shrink-0 disabled:opacity-50"
          >
            <Send size={18} className="ml-0.5" />
          </button>
        </div>
        <p className="text-[10px] text-center text-slate-400 mt-3 font-medium">
          Assist AI provides leasing guidance. Consult legal counsel for binding agreements.
        </p>
      </div>
    </div>
  );
};

export default ChatbotOverlay;
