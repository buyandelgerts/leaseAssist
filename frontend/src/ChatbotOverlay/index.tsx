import { FileText, MessageCircle, Percent, Plus, Search, Send, Settings, UploadCloud, X } from "lucide-react";

type ChatbotOverlayRoute =
  | 'home'
  | 'search'
  | 'detail'
  | 'analysis-upload'
  | 'analysis-result'
  | 'calculator';

interface ChatbotOverlayProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  setCurrentView: (view: ChatbotOverlayRoute) => void;
}

const ChatbotOverlay = ({ isOpen, setIsOpen, setCurrentView }: ChatbotOverlayProps) => {
    if (!isOpen) return null;
  
    return (
      <div className="fixed inset-0 md:inset-auto md:bottom-6 md:right-6 md:w-[600px] z-50 flex flex-col bg-white md:rounded-2xl shadow-2xl border border-slate-200 h-full md:h-[80vh] max-h-[800px] overflow-hidden animate-in slide-in-from-bottom-10 fade-in duration-300">
        
        {/* Header */}
        <div className="bg-white border-b border-slate-100 p-4 flex justify-between items-center shrink-0">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white">
                <MessageCircle size={20} />
              </div>
              <div className="absolute -bottom-1 -right-1 w-3.5 h-3.5 bg-green-500 border-2 border-white rounded-full"></div>
            </div>
            <div>
              <h3 className="font-bold text-slate-900 leading-tight">Assist AI</h3>
              <p className="text-xs text-slate-500 flex items-center gap-1">
                <span className="w-1.5 h-1.5 bg-green-500 rounded-full inline-block"></span> Online & Ready to Assist
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button title="settings" className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors">
              <Settings size={20} />
            </button>
            <button title="x"
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
            <span className="text-[10px] font-bold text-slate-400 bg-slate-100 px-3 py-1 rounded-full uppercase tracking-wider">Today</span>
          </div>
  
          {/* AI Message 1 */}
          <div className="flex gap-4">
            <div className="w-8 h-8 bg-slate-200 rounded-full flex items-center justify-center shrink-0">
              <MessageCircle size={14} className="text-slate-500" />
            </div>
            <div className="flex-1">
              <div className="bg-white border border-slate-200 rounded-2xl rounded-tl-sm p-4 text-sm text-slate-700 shadow-sm">
                Hello! I'm Assist AI. I can help you analyze lease agreements, check your eligibility for premium properties, or find your next architectural home. How can I assist you today?
              </div>
              <span className="text-[10px] text-slate-400 mt-1 block px-1">09:41 AM</span>
            </div>
          </div>
  
          {/* User Message 1 */}
          <div className="flex gap-4 flex-row-reverse">
            <div className="w-8 h-8 bg-slate-200 rounded-full flex items-center justify-center shrink-0 overflow-hidden">
               <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80" alt="User" />
            </div>
            <div className="flex-1 flex flex-col items-end">
              <div className="bg-blue-600 text-white rounded-2xl rounded-tr-sm p-4 text-sm shadow-sm max-w-[85%]">
                I'm looking at a lease for a loft in the downtown district. Can you help me check if there are any "red flags" regarding utility caps or subletting?
              </div>
              <span className="text-[10px] text-slate-400 mt-1 block px-1">09:43 AM</span>
            </div>
          </div>
  
          {/* AI Message 2 */}
          <div className="flex gap-4">
            <div className="w-8 h-8 bg-slate-200 rounded-full flex items-center justify-center shrink-0">
              <MessageCircle size={14} className="text-slate-500" />
            </div>
            <div className="flex-1 space-y-4">
              <div className="bg-white border border-slate-200 rounded-2xl rounded-tl-sm p-4 text-sm text-slate-700 shadow-sm">
                Of course. Please upload your document, or paste the text here. I will specifically scan for section 14 (Utilities) and section 22 (Assignment & Subletting).
              </div>
              
              {/* Interactive Widget inside chat */}
              <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm w-full max-w-sm">
                <div className="flex items-center gap-2 mb-4">
                  <FileText className="text-blue-600" size={18} />
                  <span className="font-bold text-slate-900 text-sm">Lease Document Analyzer</span>
                </div>
                <div 
                  className="border-2 border-dashed border-blue-200 rounded-lg p-6 flex flex-col items-center justify-center text-center hover:bg-blue-50 cursor-pointer transition-colors"
                  onClick={() => {
                    setIsOpen(false);
                    setCurrentView('analysis-upload');
                  }}
                >
                  <UploadCloud className="text-blue-400 mb-2" size={24} />
                  <span className="font-bold text-slate-700 text-sm mb-1">Drop your PDF or DOCX here</span>
                  <span className="text-xs text-slate-400 mb-3">Maximum file size: 10MB</span>
                  <button className="bg-blue-50 text-blue-700 px-4 py-1.5 rounded-md text-xs font-bold">Select File</button>
                </div>
              </div>
  
              <span className="text-[10px] text-slate-400 block px-1">09:44 AM</span>
            </div>
          </div>
  
        </div>
  
        {/* Input Area */}
        <div className="bg-white border-t border-slate-100 p-4 shrink-0">
          
          {/* Quick Suggestions */}
          <div className="flex gap-2 overflow-x-auto pb-4 no-scrollbar">
            <button onClick={() => { setIsOpen(false); setCurrentView('calculator'); }} className="shrink-0 flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-full text-xs font-semibold text-blue-700 hover:bg-blue-50 transition-colors">
              <Percent size={14} /> Check Eligibility
            </button>
            <button onClick={() => { setIsOpen(false); setCurrentView('analysis-upload'); }} className="shrink-0 flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-full text-xs font-semibold text-blue-700 hover:bg-blue-50 transition-colors">
              <FileText size={14} /> Analyze Lease
            </button>
            <button onClick={() => { setIsOpen(false); setCurrentView('search'); }} className="shrink-0 flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-full text-xs font-semibold text-blue-700 hover:bg-blue-50 transition-colors">
              <Search size={14} /> Search Apartments
            </button>
          </div>
  
          <div className="bg-slate-100 rounded-xl p-2 flex items-center gap-2">
            <button title="plus" className="p-2 text-slate-500 hover:text-slate-800 hover:bg-slate-200 rounded-lg transition-colors">
              <Plus size={20} />
            </button>
            <input 
              type="text" 
              placeholder="Ask Assist AI about leases, properties, or rules..." 
              className="flex-1 bg-transparent border-none outline-none text-sm text-slate-700 px-2 placeholder-slate-400"
            />
            <button title="send" className="w-10 h-10 bg-blue-600 text-white rounded-lg flex items-center justify-center hover:bg-blue-700 transition-colors shrink-0">
              <Send size={18} className="ml-1" />
            </button>
          </div>
          <p className="text-[10px] text-center text-slate-400 mt-3 font-medium">
            Assist AI may provide architectural and leasing insights. Please consult legal counsel for binding agreements.
          </p>
        </div>
      </div>
    );
  };

  export default ChatbotOverlay;