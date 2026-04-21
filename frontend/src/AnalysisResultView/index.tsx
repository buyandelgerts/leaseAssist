import { useState } from "react";
import { FileText, ChevronDown, AlertCircle, CheckCircle, Mail, Zap, Send, Loader2, CheckCheck } from "lucide-react";

type AnalysisResultRoute =
  | 'home'
  | 'search'
  | 'detail'
  | 'analysis-upload'
  | 'analysis-result'
  | 'calculator';

interface AnalysisResultViewProps {
  setCurrentView: (view: AnalysisResultRoute) => void;
  analysisResult: string;
  landlordEmail: string;
}

interface ParsedItem {
  title: string;
  body: string;
}

function parseNumberedItems(text: string): ParsedItem[] {
  const items: ParsedItem[] = [];
  const parts = text.split(/\n\s*\d+\.\s+/);
  for (const part of parts) {
    const trimmed = part.trim();
    if (!trimmed) continue;
    const lines = trimmed.split('\n');
    const title = lines[0].replace(/^#+\s*/, '').replace(/^\d+\.\s*/, '').trim();
    const body = lines.slice(1).join('\n').trim();
    if (title) {
      items.push({ title, body });
    }
  }
  return items;
}

const API_BASE = import.meta.env.VITE_API_URL || (window.location.port === "5173" ? "http://localhost:8000" : "");

const AnalysisResultView = ({ setCurrentView, analysisResult, landlordEmail }: AnalysisResultViewProps) => {
    const [sendStatus, setSendStatus] = useState<'idle' | 'sending' | 'sent' | 'error'>('idle');

    const handleSendEmail = async () => {
      setSendStatus('sending');
      try {
        const res = await fetch(`${API_BASE}/send-email`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            to: landlordEmail,
            subject: "Request for Lease Agreement Revisions",
            body: emailText,
          }),
        });
        if (!res.ok) throw new Error("Failed");
        setSendStatus('sent');
      } catch {
        setSendStatus('error');
      }
    };

    // Split result into sections
    const lower = analysisResult.toLowerCase();
    const redIdx = lower.indexOf('red flag');
    const greenIdx = lower.indexOf('green flag');

    // Find email start — look for these markers AFTER the green flags section
    const searchFrom = greenIdx !== -1 ? greenIdx : 0;
    const candidates = [
      lower.indexOf('draft email', searchFrom),
      lower.indexOf('section 3', searchFrom),
      lower.indexOf('subject:', searchFrom),
      lower.indexOf('dear ', searchFrom),
    ].filter(i => i !== -1);
    const emailIdx = candidates.length > 0 ? Math.min(...candidates) : -1;

    let redText = '';
    let greenText = '';
    let emailText = '';

    if (redIdx !== -1 && greenIdx !== -1) {
      redText = analysisResult.slice(redIdx, greenIdx);
      greenText = analysisResult.slice(greenIdx, emailIdx !== -1 ? emailIdx : undefined);
    } else if (redIdx !== -1) {
      redText = analysisResult.slice(redIdx, emailIdx !== -1 ? emailIdx : undefined);
    }
    if (emailIdx !== -1) {
      emailText = analysisResult.slice(emailIdx);
    }

    // Remove section headers and "SECTION N —" markers
    const cleanSection = (s: string) => s
      .replace(/^.*?(red|green)\s*flag[^\n]*\n?/i, '')
      .replace(/\n?\s*SECTION\s+\d+\s*[-—][^\n]*/gi, '')
      .trim();

    redText = cleanSection(redText);
    greenText = cleanSection(greenText);
    emailText = emailText
      .replace(/^.*?draft email[^\n]*\n?/i, '')
      .replace(/^.*?SECTION\s+\d+\s*[-—][^\n]*\n?/i, '')
      .trim();

    const redItems = parseNumberedItems(redText);
    const greenItems = parseNumberedItems(greenText);

    return (
      <div className="flex flex-col lg:flex-row min-h-[calc(100vh-64px)] bg-slate-50">
        {/* Sidebar */}
        <div className="w-full lg:w-64 bg-white border-r border-slate-200 p-6 hidden lg:block shrink-0">
          <div className="mb-8">
            <h2 className="text-lg font-bold text-blue-900 mb-1">Curated Spaces</h2>
            <p className="text-xs text-slate-500 uppercase tracking-widest font-semibold">Premium Tier</p>
          </div>
          <nav className="space-y-2">
             <a href="#" className="flex items-center gap-3 px-3 py-2.5 bg-blue-50 text-blue-700 rounded-lg font-medium transition-colors">
              <FileText size={18} /> My Documents
            </a>
          </nav>
        </div>

        <div className="flex-1 p-6 md:p-12 max-w-5xl mx-auto w-full">
          {/* Header */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-10 gap-6">
            <div>
              <div className="flex items-center gap-2 text-sm text-slate-500 mb-4">
                <span className="hover:text-blue-600 cursor-pointer" onClick={() => setCurrentView('analysis-upload')}>Documents</span>
                <ChevronDown className="rotate-270" size={14} />
                <span>Lease Agreement</span>
                <ChevronDown className="rotate-270" size={14} />
                <span className="font-semibold text-slate-900">Analysis Results</span>
              </div>
              <h1 className="text-4xl font-bold text-slate-900 mb-3">Lease Analysis Results</h1>
              <p className="text-slate-600 max-w-2xl">
                We've audited your lease agreement. Below are the findings regarding financial transparency and legal safeguards.
              </p>
            </div>

            {/* Trust Score Donut */}
            {redItems.length + greenItems.length > 0 && (() => {
              const total = redItems.length + greenItems.length;
              const redPercent = Math.round((redItems.length / total) * 100);
              const greenPercent = 100 - redPercent;
              const circumference = 2 * Math.PI * 54;
              const greenArc = (greenPercent / 100) * circumference;
              const greenStart = (redPercent / 100) * circumference;
              return (
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm shrink-0 flex flex-col items-center">
                  <div className="flex items-center justify-between w-full mb-4">
                    <span className="text-[10px] font-bold text-rose-600 bg-rose-50 px-2 py-1 rounded-full">RED FLAG</span>
                    <span className="text-[10px] font-bold text-green-600 bg-green-50 px-2 py-1 rounded-full">GREEN FLAG</span>
                  </div>
                  <div className="relative w-36 h-36">
                    <svg className="w-36 h-36 -rotate-90" viewBox="0 0 120 120">
                      <circle cx="60" cy="60" r="54" fill="none" stroke="#e2e8f0" strokeWidth="8" />
                      {/* Red arc */}
                      <circle
                        cx="60" cy="60" r="54" fill="none"
                        stroke="#e11d48" strokeWidth="8"
                        strokeDasharray={`${(redPercent / 100) * circumference} ${circumference}`}
                        strokeDashoffset="0"
                      />
                      {/* Green arc */}
                      <circle
                        cx="60" cy="60" r="54" fill="none"
                        stroke="#16a34a" strokeWidth="8"
                        strokeDasharray={`${greenArc} ${circumference}`}
                        strokeDashoffset={-greenStart}
                      />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className="text-lg font-bold text-slate-900">{total} Flags</span>
                    </div>
                  </div>
                  <div className="flex gap-4 mt-4">
                    <div className="flex items-center gap-1.5">
                      <div className="w-3 h-3 rounded-full bg-rose-600"></div>
                      <span className="text-xs font-bold text-slate-700">{redItems.length} Red ({redPercent}%)</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div className="w-3 h-3 rounded-full bg-green-600"></div>
                      <span className="text-xs font-bold text-slate-700">{greenItems.length} Green ({greenPercent}%)</span>
                    </div>
                  </div>
                </div>
              );
            })()}
          </div>

          {/* Red & Green Flags Side by Side */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-8 mb-12">

            {/* Red Flags */}
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center">
                  <AlertCircle size={20} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900">Red Flags</h3>
                  <p className="text-sm text-slate-500">Critical clauses requiring immediate clarification</p>
                </div>
              </div>
              <div className="space-y-4">
                {redItems.map((item, i) => (
                  <div key={i} className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                    <div className="bg-rose-50 border-b border-rose-100 px-5 py-3">
                      <h4 className="font-bold text-rose-900 text-sm">{item.title}</h4>
                    </div>
                    <div className="px-5 py-4">
                      <p className="text-sm text-slate-700 leading-relaxed">{item.body.replace(/^\s+/gm, '')}</p>
                    </div>
                  </div>
                ))}
                {redItems.length === 0 && (
                  <div className="bg-green-50 border border-green-200 rounded-xl p-6 text-center">
                    <p className="text-sm text-green-700 font-medium">No red flags identified.</p>
                  </div>
                )}
              </div>
            </div>

            {/* Green Flags */}
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-green-100 text-green-600 rounded-full flex items-center justify-center">
                  <CheckCircle size={20} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900">Green Flags</h3>
                  <p className="text-sm text-slate-500">Standard or favorable terms for the tenant</p>
                </div>
              </div>
              <div className="space-y-4">
                {greenItems.map((item, i) => (
                  <div key={i} className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                    <div className="bg-green-50 border-b border-green-100 px-5 py-3">
                      <h4 className="font-bold text-green-900 text-sm">{item.title}</h4>
                    </div>
                    <div className="px-5 py-4">
                      <p className="text-sm text-slate-700 leading-relaxed">{item.body.replace(/^\s+/gm, '')}</p>
                    </div>
                  </div>
                ))}
                {greenItems.length === 0 && (
                  <div className="bg-slate-50 border border-slate-200 rounded-xl p-6 text-center">
                    <p className="text-sm text-slate-500">No green flags identified.</p>
                  </div>
                )}
              </div>
            </div>

          </div>

          {/* Email Draft */}
          {emailText && (
            <div className="bg-white border border-slate-200 rounded-2xl p-8 mb-12 shadow-sm">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center">
                  <Mail size={20} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900">Draft Email to Landlord</h3>
                  <p className="text-sm text-slate-500">Auto-generated negotiation email based on the red flags above</p>
                </div>
              </div>
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-6">
                <pre className="whitespace-pre-wrap text-sm text-slate-700 font-sans leading-relaxed">{emailText}</pre>
              </div>
              <div className="mt-4 flex justify-end">
                <button
                  onClick={handleSendEmail}
                  disabled={sendStatus === 'sending' || sendStatus === 'sent'}
                  className={`px-6 py-3 rounded-xl font-bold transition-colors shadow-md flex items-center gap-2 disabled:cursor-not-allowed ${
                    sendStatus === 'sent' ? 'bg-green-600 text-white' :
                    sendStatus === 'error' ? 'bg-rose-600 text-white hover:bg-rose-700' :
                    'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                >
                  {sendStatus === 'sending' && <><Loader2 size={18} className="animate-spin" /> Sending...</>}
                  {sendStatus === 'sent' && <><CheckCheck size={18} /> Email Sent!</>}
                  {sendStatus === 'error' && <><Send size={18} /> Retry Send</>}
                  {sendStatus === 'idle' && <><Send size={18} /> Send Email to Landlord</>}
                </button>
              </div>
            </div>
          )}

          {/* Bottom Action Bar */}
          <div className="flex flex-col md:flex-row gap-6">
            <div className="flex-1 bg-white border border-slate-200 rounded-2xl p-8 flex flex-col justify-center">
              <h3 className="text-xl font-bold text-slate-900 mb-4">What's Next?</h3>
              <p className="text-sm text-slate-600">Review the red flags above and use the draft email to negotiate with your landlord. Consult a licensed attorney for binding legal interpretation.</p>
            </div>

            <div className="md:w-80 bg-blue-600 rounded-2xl p-8 text-white flex flex-col justify-center shadow-lg relative overflow-hidden">
               <div className="absolute -top-10 -right-10 opacity-10">
                 <Zap size={150} />
               </div>
               <div className="relative z-10">
                 <Zap className="mb-4" size={32} />
                 <h3 className="text-2xl font-bold mb-2">Re-analyze?</h3>
                 <p className="text-blue-100 text-sm mb-6">Upload a revised lease or change your city to compare against different laws.</p>
                 <button
                   onClick={() => setCurrentView('analysis-upload')}
                   className="w-full bg-white text-blue-600 py-3 rounded-xl font-bold hover:bg-slate-50 transition-colors shadow-md"
                 >
                   Back to Upload
                 </button>
               </div>
            </div>
          </div>

        </div>
      </div>
    );
  };

  export default AnalysisResultView;
