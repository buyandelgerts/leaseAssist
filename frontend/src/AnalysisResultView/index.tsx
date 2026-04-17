import { FileText, ChevronDown, AlertCircle, CheckCircle, Zap } from "lucide-react";
import { ANALYSIS_FLAGS } from "../mockData";

type AnalysisResultRoute =
  | 'home'
  | 'search'
  | 'detail'
  | 'analysis-upload'
  | 'analysis-result'
  | 'calculator';

interface AnalysisResultViewProps {
  setCurrentView: (view: AnalysisResultRoute) => void;
}

const AnalysisResultView = ({ setCurrentView }: AnalysisResultViewProps) => {
    return (
      <div className="flex flex-col lg:flex-row min-h-[calc(100vh-64px)] bg-slate-50">
        {/* Sidebar - Same as Upload view */}
        <div className="w-full lg:w-64 bg-white border-r border-slate-200 p-6 hidden lg:block shrink-0">
          <div className="mb-8">
            <h2 className="text-lg font-bold text-blue-900 mb-1">Curated Spaces</h2>
            <p className="text-xs text-slate-500 uppercase tracking-widest font-semibold">Premium Tier</p>
          </div>
          <nav className="space-y-2">
             {/* ... standard sidebar links ... */}
             <a href="#" className="flex items-center gap-3 px-3 py-2.5 bg-blue-50 text-blue-700 rounded-lg font-medium transition-colors">
              <FileText size={18} /> My Documents
            </a>
          </nav>
        </div>
  
        <div className="flex-1 p-6 md:p-12 max-w-5xl mx-auto w-full">
          {/* Header Area */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-10 gap-6">
            <div>
              <div className="flex items-center gap-2 text-sm text-slate-500 mb-4">
                <span className="hover:text-blue-600 cursor-pointer" onClick={() => setCurrentView('analysis-upload')}>Documents</span>
                <ChevronDown className="rotate-270" size={14} />
                <span>The Lumina Penthouse - Lease Agreement</span>
                <ChevronDown className="rotate-270" size={14} />
                <span className="font-semibold text-slate-900">Analysis Results</span>
              </div>
              <h1 className="text-4xl font-bold text-slate-900 mb-3">Lease Analysis Results</h1>
              <p className="text-slate-600 max-w-2xl">
                We've audited your lease for the <strong>Lumina Penthouse, Unit 402</strong>. Below are the architectural findings regarding financial transparency and legal safeguards.
              </p>
            </div>
            
            {/* Trust Score */}
            <div className="bg-white border border-slate-200 rounded-2xl p-4 flex items-center gap-4 shadow-sm shrink-0">
              <div className="relative w-16 h-16 rounded-full border-4 border-green-500 flex items-center justify-center">
                <span className="text-2xl font-bold text-slate-900">75</span>
              </div>
              <div>
                <span className="text-[10px] font-bold text-slate-500 tracking-wider uppercase block">Aura Trust Score</span>
                <span className="text-lg font-bold text-green-600">Strong<br/>Agreement</span>
              </div>
            </div>
          </div>
  
          {/* Flags Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-12 mb-12">
            
            {/* Red Flags Column */}
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
                {ANALYSIS_FLAGS.filter(f => f.type === 'red').map(flag => (
                  <div key={flag.id} className="bg-white border-l-4 border-rose-500 rounded-r-xl border-y border-r border-slate-200 p-6 shadow-sm relative overflow-hidden">
                    <div className="flex justify-between items-start mb-3">
                      <span className="bg-rose-500 text-white text-[10px] font-bold px-2.5 py-1 rounded-full tracking-wider uppercase">{flag.tag}</span>
                      <span className="text-xs font-semibold text-slate-400">{flag.section}</span>
                    </div>
                    <h4 className="text-lg font-bold text-slate-900 mb-2">{flag.title}</h4>
                    <p className="text-sm text-slate-600 mb-4">{flag.text}</p>
                    <div className="bg-rose-50 p-3 rounded-lg flex gap-2 items-start border border-rose-100">
                      <AlertCircle className="text-rose-600 mt-0.5 shrink-0" size={16} />
                      <p className="text-sm font-semibold text-rose-900">Action: {flag.action}</p>
                    </div>
                  </div>
                ))}
  
                <div className="bg-slate-100/50 border border-slate-200 border-dashed rounded-xl p-6 text-center">
                  <h5 className="font-bold text-slate-700 mb-1">Legal Review Required</h5>
                  <p className="text-xs text-slate-500">These flags represent significant financial or legal risk to the tenant.</p>
                </div>
              </div>
            </div>
  
            {/* Green Flags Column */}
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
                {ANALYSIS_FLAGS.filter(f => f.type === 'green').map(flag => (
                  <div key={flag.id} className="bg-white border-l-4 border-green-500 rounded-r-xl border-y border-r border-slate-200 p-6 shadow-sm">
                    <div className="flex justify-between items-start mb-3">
                      <span className="bg-green-100 text-green-800 text-[10px] font-bold px-2.5 py-1 rounded-full tracking-wider uppercase">{flag.tag}</span>
                      <span className="text-xs font-semibold text-slate-400">{flag.section}</span>
                    </div>
                    <h4 className="text-lg font-bold text-slate-900 mb-2">{flag.title}</h4>
                    <p className="text-sm text-slate-600 mb-4">{flag.text}</p>
                    <div className="bg-green-50 p-3 rounded-lg flex gap-2 items-start border border-green-100">
                      <CheckCircle className="text-green-600 mt-0.5 shrink-0" size={16} />
                      <p className="text-sm font-semibold text-green-900">Benefit: {flag.action}</p>
                    </div>
                  </div>
                ))}
  
                {/* Subject Property Mini-Card */}
                <div className="rounded-xl overflow-hidden relative h-40 group cursor-pointer" onClick={() => setCurrentView('detail')}>
                  <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Building" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-900 to-transparent"></div>
                  <div className="absolute bottom-4 left-4">
                    <span className="text-[10px] font-bold text-white/70 tracking-wider uppercase block mb-1">Subject Property</span>
                    <h5 className="font-bold text-white">Lumina Penthouse, Unit 402</h5>
                  </div>
                </div>
              </div>
            </div>
  
          </div>
  
          {/* Bottom Summary Bar */}
          <div className="flex flex-col md:flex-row gap-6">
            <div className="flex-1 bg-white border border-slate-200 rounded-2xl p-8 flex flex-col justify-center">
              <h3 className="text-xl font-bold text-slate-900 mb-6">Analysis Summary</h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-6">
                <div>
                  <span className="text-[10px] font-bold text-slate-400 tracking-wider uppercase block mb-1">Total Flags</span>
                  <span className="text-3xl font-bold text-slate-900">12</span>
                </div>
                <div>
                  <span className="text-[10px] font-bold text-rose-500 tracking-wider uppercase block mb-1">High Risk</span>
                  <span className="text-3xl font-bold text-rose-600">2</span>
                </div>
                <div>
                  <span className="text-[10px] font-bold text-green-500 tracking-wider uppercase block mb-1">Favorable</span>
                  <span className="text-3xl font-bold text-green-600">8</span>
                </div>
                <div>
                  <span className="text-[10px] font-bold text-slate-400 tracking-wider uppercase block mb-1">Neutral</span>
                  <span className="text-3xl font-bold text-slate-600">2</span>
                </div>
              </div>
            </div>
            
            <div className="md:w-80 bg-blue-600 rounded-2xl p-8 text-white flex flex-col justify-center shadow-lg relative overflow-hidden">
               <div className="absolute -top-10 -right-10 opacity-10">
                 <Zap size={150} />
               </div>
               <div className="relative z-10">
                 <Zap className="mb-4" size={32} />
                 <h3 className="text-2xl font-bold mb-2">Ready to Proceed?</h3>
                 <p className="text-blue-100 text-sm mb-6">Generate a list of counter-questions for the landlord based on these flags.</p>
                 <button className="w-full bg-white text-blue-600 py-3 rounded-xl font-bold hover:bg-slate-50 transition-colors shadow-md">
                   Generate PDF Memo
                 </button>
               </div>
            </div>
          </div>
  
        </div>
      </div>
    );
  };

  export default AnalysisResultView;