import { useEffect, useRef, useState } from "react";
import {
  Bath,
  BedDouble,
  FileText,
  MessageCircle,
  Percent,
  Plus,
  Search,
  Send,
  Settings,
  X,
} from "lucide-react";
import type { SelectedProperty } from "../App";

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

interface ApartmentResult {
  id: string | number;
  formatted_address: string;
  city: string;
  state: string;
  zip_code?: string;
  price?: number | string;
  bedrooms?: number | string;
  bathrooms?: number | string;
  square_footage?: number | string;
  property_type?: string;
  content?: string;
  similarity_score?: number | null;
}

interface RouteButton {
  label: string;
  route: "calculator" | "analysis-upload";
}

interface Message {
  id: string;
  role: "user" | "assistant";
  text: string;
  timestamp: Date;
  type?: "text" | "apartments" | "route";
  apartments?: ApartmentResult[];
  buttons?: RouteButton[];
}

interface ChatbotOverlayProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  setCurrentView: (view: ChatbotOverlayRoute) => void;
  setSelectedProperty: (property: SelectedProperty) => void;
  sessionContext?: SessionContext;
}

const QUICK_PROMPTS = [
  { label: "Find apartments in Austin under $2000", icon: <Search size={14} /> },
  { label: "Is a 3-month security deposit legal in California?", icon: <FileText size={14} /> },
  { label: "Summarize my eligibility results", icon: <Percent size={14} /> },
  { label: "Walk me through my lease red flags", icon: <MessageCircle size={14} /> },
];

const AI_SERVICE_URL = "http://localhost:8000";

function parseNum(v?: number | string): number {
  if (typeof v === "number") return v;
  if (typeof v === "string") {
    const x = parseFloat(v.replace(/[^0-9.-]/g, ""));
    return isNaN(x) ? 0 : x;
  }
  return 0;
}

function toSelectedProperty(apt: ApartmentResult): SelectedProperty {
  return {
    id: apt.id,
    title: apt.property_type || "Rental Property",
    location: apt.formatted_address || [apt.city, apt.state].filter(Boolean).join(", "),
    price: parseNum(apt.price),
    beds: parseNum(apt.bedrooms),
    baths: parseNum(apt.bathrooms),
    sqft: parseNum(apt.square_footage),
    image:
      "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
    summary: apt.content || "",
  };
}

const ApartmentChatCard = ({
  apt,
  onClick,
}: {
  apt: ApartmentResult;
  onClick: () => void;
}) => {
  const price = parseNum(apt.price);
  const beds = parseNum(apt.bedrooms);
  const baths = parseNum(apt.bathrooms);

  return (
    <div
      onClick={onClick}
      className="bg-white border border-slate-200 rounded-xl p-3 cursor-pointer hover:border-blue-400 hover:shadow-md transition-all group"
    >
      <p className="text-xs font-semibold text-slate-800 leading-snug group-hover:text-blue-600 line-clamp-2">
        {apt.formatted_address || [apt.city, apt.state].filter(Boolean).join(", ")}
      </p>
      <p className="text-base font-bold text-blue-600 mt-1">
        ${price > 0 ? price.toLocaleString() : "—"}
        <span className="text-xs font-normal text-slate-500">/mo</span>
      </p>
      <div className="flex items-center gap-3 mt-1.5 text-xs text-slate-500">
        {beds > 0 && (
          <span className="flex items-center gap-1">
            <BedDouble size={12} />
            {beds} bd
          </span>
        )}
        {baths > 0 && (
          <span className="flex items-center gap-1">
            <Bath size={12} />
            {baths} ba
          </span>
        )}
      </div>
      <p className="text-[10px] text-blue-500 mt-1.5 font-medium">Tap to view details →</p>
    </div>
  );
};

const ChatbotOverlay = ({
  isOpen,
  setIsOpen,
  setCurrentView,
  setSelectedProperty,
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
      const raw = data?.result;

      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        text: "",
        timestamp: new Date(),
      };

      // Normalise: backend may return a plain object or a JSON string
      let payload: Record<string, unknown> | null = null;
      if (raw && typeof raw === "object") {
        payload = raw as Record<string, unknown>;
      } else if (typeof raw === "string") {
        try { payload = JSON.parse(raw); } catch { /* fall through */ }
      }

      if (payload && "type" in payload) {
        assistantMsg.type = payload.type as Message["type"];
        assistantMsg.text = (payload.message as string) ?? "";
        if (payload.type === "apartments" && Array.isArray(payload.apartments)) {
          assistantMsg.apartments = payload.apartments as ApartmentResult[];
        }
        if (payload.type === "route" && Array.isArray(payload.buttons)) {
          assistantMsg.buttons = payload.buttons as RouteButton[];
        }
      } else {
        assistantMsg.text =
          typeof raw === "string" ? raw : "Sorry, I couldn't get a response.";
      }

      setMessages((prev) => [...prev, assistantMsg]);
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
                msg.role === "assistant" ? "bg-slate-200" : "bg-blue-100"
              }`}
            >
              <MessageCircle
                size={14}
                className={msg.role === "assistant" ? "text-slate-500" : "text-blue-600"}
              />
            </div>
            <div className={`flex-1 ${msg.role === "user" ? "flex flex-col items-end" : ""}`}>
              <div
                className={`rounded-2xl p-4 text-sm shadow-sm max-w-[85%] ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white rounded-tr-sm whitespace-pre-wrap"
                    : "bg-white border border-slate-200 text-slate-700 rounded-tl-sm"
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.text}</p>

                {msg.type === "apartments" && msg.apartments && msg.apartments.length > 0 && (
                  <div className="mt-3 space-y-2">
                    {msg.apartments.map((apt) => (
                      <ApartmentChatCard
                        key={apt.id}
                        apt={apt}
                        onClick={() => {
                          setSelectedProperty(toSelectedProperty(apt));
                          setCurrentView("detail");
                          setIsOpen(false);
                        }}
                      />
                    ))}
                  </div>
                )}

                {msg.type === "route" && msg.buttons && msg.buttons.length > 0 && (
                  <div className="mt-3 flex flex-col gap-2">
                    {msg.buttons.map((btn) => (
                      <button
                        key={btn.route}
                        onClick={() => {
                          setCurrentView(btn.route);
                          setIsOpen(false);
                        }}
                        className="w-full bg-blue-600 text-white text-sm font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-left"
                      >
                        {btn.label} →
                      </button>
                    ))}
                  </div>
                )}
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
          {/* <button
            onClick={() => { setIsOpen(false); setCurrentView("calculator"); }}
            className="shrink-0 flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-full text-xs font-semibold text-blue-700 hover:bg-blue-50 transition-colors"
          >
            <Percent size={14} /> Check Eligibility
          </button> */}
          {/* <button
            onClick={() => { setIsOpen(false); setCurrentView("analysis-upload"); }}
            className="shrink-0 flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-full text-xs font-semibold text-blue-700 hover:bg-blue-50 transition-colors"
          >
            <FileText size={14} /> Analyze Lease
          </button> */}
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
