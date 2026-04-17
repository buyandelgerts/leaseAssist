import { Map, Bookmark, File, FileText, HelpCircle, UploadCloud, Shield, Zap, DollarSign, AlertCircle, Building2, ArrowRight } from "lucide-react";

type AnalysisUploadRoute =
  | 'home'
  | 'search'
  | 'detail'
  | 'analysis-upload'
  | 'analysis-result'
  | 'calculator';

interface AnalysisUploadViewProps {
  setCurrentView: (view: AnalysisUploadRoute) => void;
}

const AnalysisUploadView = ({ setCurrentView }: AnalysisUploadViewProps) => {
    return (
      <div className="flex flex-col lg:flex-row min-h-[calc(100vh-64px)] bg-slate-50">
        
        {/* Sidebar Navigation */}
        <div className="w-full lg:w-64 bg-white border-r border-slate-200 p-6 hidden lg:block shrink-0">
          <div className="mb-8">
            <h2 className="text-lg font-bold text-blue-900 mb-1">Curated Spaces</h2>
            <p className="text-xs text-slate-500 uppercase tracking-widest font-semibold">Premium Tier</p>
          </div>
          <nav className="space-y-2">
            <a href="#" className="flex items-center gap-3 px-3 py-2.5 text-slate-600 hover:bg-slate-50 rounded-lg font-medium transition-colors">
              <Map size={18} /> Map View
            </a>
            <a href="#" className="flex items-center gap-3 px-3 py-2.5 text-slate-600 hover:bg-slate-50 rounded-lg font-medium transition-colors">
              <Bookmark size={18} /> Saved Properties
            </a>
            <a href="#" className="flex items-center gap-3 px-3 py-2.5 bg-blue-50 text-blue-700 rounded-lg font-medium transition-colors">
              <FileText size={18} /> My Documents
            </a>
            <a href="#" className="flex items-center gap-3 px-3 py-2.5 text-slate-600 hover:bg-slate-50 rounded-lg font-medium transition-colors mt-8">
              <HelpCircle size={18} /> Support
            </a>
          </nav>
        </div>
  
        {/* Main Content */}
        <div className="flex-1 p-6 md:p-12 max-w-5xl mx-auto w-full">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-slate-900 mb-2">Leasing Document Center</h1>
            <p className="text-slate-600">Upload your lease agreement to reveal hidden clauses, financial insights, and potential red flags.</p>
          </div>
  
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Upload Area */}
            <div className="lg:col-span-2 space-y-6">
              
              {/* Drag & Drop */}
              <div className="bg-white border-2 border-dashed border-blue-200 rounded-2xl p-12 flex flex-col items-center justify-center text-center hover:bg-blue-50/50 transition-colors cursor-pointer group">
                <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <UploadCloud size={32} />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">Upload Document</h3>
                <p className="text-slate-500 mb-6 max-w-sm">Drag and drop your lease agreement here or click to browse files</p>
                <div className="flex gap-3">
                  <span className="bg-slate-100 text-slate-600 text-xs font-bold px-3 py-1.5 rounded-md">PDF</span>
                  <span className="bg-slate-100 text-slate-600 text-xs font-bold px-3 py-1.5 rounded-md">DOCX</span>
                </div>
              </div>
  
              {/* Manual Entry */}
              <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="font-bold text-slate-900">Paste Lease Text</h3>
                  <span className="text-xs font-bold text-slate-400 bg-slate-100 px-2 py-1 rounded">MANUAL ENTRY</span>
                </div>
                <textarea 
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm text-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[200px]"
                  placeholder="Paste the legal text of your lease agreement here for a quick scan..."
                ></textarea>
              </div>
  
              {/* Info Badges */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4">
                 <div className="bg-white p-4 rounded-xl border border-slate-200 flex items-center gap-3">
                   <Shield className="text-blue-600" size={20} />
                   <div>
                     <h5 className="font-bold text-slate-900 text-sm">Encrypted Storage</h5>
                     <p className="text-xs text-slate-500">Bank-level security</p>
                   </div>
                 </div>
                 <div className="bg-white p-4 rounded-xl border border-slate-200 flex items-center gap-3">
                   <File className="text-blue-600" size={20} />
                   <div>
                     <h5 className="font-bold text-slate-900 text-sm">Multiple Formats</h5>
                     <p className="text-xs text-slate-500">PDF, Word, or Scans</p>
                   </div>
                 </div>
                 <div className="bg-white p-4 rounded-xl border border-slate-200 flex items-center gap-3">
                   <Zap className="text-blue-600" size={20} />
                   <div>
                     <h5 className="font-bold text-slate-900 text-sm">Instant Results</h5>
                     <p className="text-xs text-slate-500">AI-powered extraction</p>
                   </div>
                 </div>
              </div>
  
            </div>
  
            {/* Strategy Sidebar */}
            <div className="lg:col-span-1 space-y-6">
              <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
                <h3 className="font-bold text-slate-900 mb-6">Analysis Strategy</h3>
                
                <div className="space-y-6 mb-8">
                  <div className="flex gap-4">
                    <div className="w-10 h-10 bg-green-100 text-green-600 rounded-full flex items-center justify-center shrink-0">
                      <DollarSign size={20} />
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-900 text-sm">Financial Audit</h4>
                      <p className="text-xs text-slate-500 mt-1">Calculation of total lease costs, security deposits, and hidden fees.</p>
                    </div>
                  </div>
                  <div className="flex gap-4">
                    <div className="w-10 h-10 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center shrink-0">
                      <AlertCircle size={20} />
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-900 text-sm">Red Flag Detection</h4>
                      <p className="text-xs text-slate-500 mt-1">Identification of predatory clauses or unusual termination terms.</p>
                    </div>
                  </div>
                  <div className="flex gap-4">
                    <div className="w-10 h-10 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center shrink-0">
                      <Building2 size={20} />
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-900 text-sm">Local Compliance</h4>
                      <p className="text-xs text-slate-500 mt-1">Comparing terms against current state and city housing laws.</p>
                    </div>
                  </div>
                </div>
  
                <button 
                  onClick={() => setCurrentView('analysis-result')}
                  className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition-colors shadow-md flex items-center justify-center gap-2"
                >
                  Analyze Lease <ArrowRight size={18} />
                </button>
              </div>
  
              <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 text-white overflow-hidden relative">
                <div className="absolute top-0 right-0 opacity-20 transform translate-x-4 -translate-y-4">
                  <Shield size={100} />
                </div>
                <div className="relative z-10">
                  <span className="text-xs font-bold text-green-400 tracking-wider uppercase mb-2 block">Pro Tip</span>
                  <p className="text-sm text-slate-300 leading-relaxed">
                    Ensure all pages including the <strong>Schedule of Equipment</strong> and <strong>Maintenance Riders</strong> are included for the most accurate financial analysis.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  export default AnalysisUploadView;