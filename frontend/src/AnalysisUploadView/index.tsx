import { useState, useRef, useEffect } from "react";
import { File, UploadCloud, Shield, Zap, DollarSign, AlertCircle, Building2, ArrowRight, Loader2 } from "lucide-react";
import * as pdfjsLib from "pdfjs-dist";
import pdfjsWorker from "pdfjs-dist/build/pdf.worker.min.mjs?url";
import mammoth from "mammoth";

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;

type AnalysisUploadRoute =
  | 'home'
  | 'search'
  | 'detail'
  | 'analysis-upload'
  | 'analysis-result'
  | 'calculator';

interface AnalysisUploadViewProps {
  setCurrentView: (view: AnalysisUploadRoute) => void;
  setAnalysisResult: (result: string) => void;
  analysisLoading: boolean;
  setAnalysisLoading: (loading: boolean) => void;
}

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

const AnalysisUploadView = ({ setCurrentView, setAnalysisResult, analysisLoading, setAnalysisLoading }: AnalysisUploadViewProps) => {
    const [inputMode, setInputMode] = useState<'upload' | 'paste'>('paste');
    const [error, setError] = useState<string | null>(null);
    const [agentStep, setAgentStep] = useState(0);
    const [uploadedText, setUploadedText] = useState("");
    const [uploadedFileName, setUploadedFileName] = useState("");
    const leaseTextRef = useRef<HTMLTextAreaElement>(null);
    const cityRef = useRef<HTMLInputElement>(null);
    const emailRef = useRef<HTMLInputElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const extractTextFromFile = async (file: globalThis.File) => {
      const name = file.name.toLowerCase();
      setUploadedFileName(file.name);
      setError(null);

      try {
        if (name.endsWith('.txt')) {
          const text = await file.text();
          setUploadedText(text);
        } else if (name.endsWith('.pdf')) {
          const buffer = await file.arrayBuffer();
          const pdf = await pdfjsLib.getDocument({ data: buffer }).promise;
          let text = '';
          for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const content = await page.getTextContent();
            text += content.items.map((item) => ('str' in item ? item.str : '')).join(' ') + '\n';
          }
          setUploadedText(text.trim());
        } else if (name.endsWith('.docx') || name.endsWith('.doc')) {
          const buffer = await file.arrayBuffer();
          const result = await mammoth.extractRawText({ arrayBuffer: buffer });
          setUploadedText(result.value);
        } else {
          setError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.");
        }
      } catch {
        setError("Failed to read the file. Please try pasting the text instead.");
      }
    };

    const handleFileDrop = (e: React.DragEvent) => {
      e.preventDefault();
      const file = e.dataTransfer.files[0];
      if (file) extractTextFromFile(file);
    };

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) extractTextFromFile(file);
    };

    const AGENT_STEPS = [
      "Lease Data Extractor",
      "Lease Clause Extractor",
      "Lease Red Flag Detector",
      "Market Comparison Analyst",
      "Lease Negotiation Advisor",
    ];

    useEffect(() => {
      if (!analysisLoading) {
        setAgentStep(0);
        return;
      }
      const interval = setInterval(() => {
        setAgentStep(prev => (prev < AGENT_STEPS.length - 1 ? prev + 1 : prev));
      }, 15000); // ~15s per agent
      return () => clearInterval(interval);
    }, [analysisLoading]);

    const handleAnalyze = async () => {
      const leaseText = inputMode === 'paste'
        ? (leaseTextRef.current?.value || "")
        : uploadedText;
      const cityName = cityRef.current?.value || "California";
      const landlordEmail = emailRef.current?.value || "";

      if (!leaseText.trim()) {
        setError(inputMode === 'paste'
          ? "Please paste your lease text before analyzing."
          : "Please upload a document first.");
        return;
      }

      setError(null);
      setAnalysisLoading(true);

      try {
        const res = await fetch(`${API_BASE}/analyze-lease`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            inputType: "text",
            leaseInput: leaseText,
            cityName,
            landlordEmail,
          }),
        });

        if (!res.ok) throw new Error(`API error: ${res.status}`);

        const data = await res.json();
        if (data.status === "success" && data.result) {
          setAnalysisResult(data.result);
        } else {
          setError("Unexpected response format from the server.");
          return;
        }
        setCurrentView('analysis-result');
      } catch (err) {
        setError("Failed to connect to the analysis server. Please ensure the backend is running.");
      } finally {
        setAnalysisLoading(false);
      }
    };

    return (
      <div className="flex flex-col lg:flex-row min-h-[calc(100vh-64px)] bg-slate-50">
        {/* Main Content */}
        <div className="flex-1 p-6 md:p-12 max-w-5xl mx-auto w-full">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-slate-900 mb-2">Leasing Document Center</h1>
            <p className="text-slate-600">Upload your lease agreement to reveal hidden clauses, financial insights, and potential red flags.</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Upload Area */}
            <div className="lg:col-span-2 space-y-6">

              {/* Input Mode Radio Toggle */}
              <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex gap-6">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="inputMode"
                    value="upload"
                    checked={inputMode === 'upload'}
                    onChange={() => setInputMode('upload')}
                    className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                  />
                  <span className={`font-bold text-sm ${inputMode === 'upload' ? 'text-blue-700' : 'text-slate-600'}`}>
                    Document Upload
                  </span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="inputMode"
                    value="paste"
                    checked={inputMode === 'paste'}
                    onChange={() => setInputMode('paste')}
                    className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                  />
                  <span className={`font-bold text-sm ${inputMode === 'paste' ? 'text-blue-700' : 'text-slate-600'}`}>
                    Paste Text
                  </span>
                </label>
              </div>

              {/* Drag & Drop (shown when upload is selected) */}
              {inputMode === 'upload' && (
                <>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.docx,.doc,.txt"
                    className="hidden"
                    onChange={handleFileSelect}
                  />
                  <div
                    onClick={() => fileInputRef.current?.click()}
                    onDrop={handleFileDrop}
                    onDragOver={(e) => e.preventDefault()}
                    className="bg-white border-2 border-dashed border-blue-200 rounded-2xl p-12 flex flex-col items-center justify-center text-center hover:bg-blue-50/50 transition-colors cursor-pointer group"
                  >
                    <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                      <UploadCloud size={32} />
                    </div>
                    {uploadedFileName ? (
                      <>
                        <h3 className="text-xl font-bold text-green-700 mb-2">{uploadedFileName}</h3>
                        <p className="text-slate-500 mb-2">File loaded — {uploadedText.length} characters extracted</p>
                        <p className="text-xs text-slate-400">Click to upload a different file</p>
                      </>
                    ) : (
                      <>
                        <h3 className="text-xl font-bold text-slate-900 mb-2">Upload Document</h3>
                        <p className="text-slate-500 mb-6 max-w-sm">Drag and drop your lease agreement here or click to browse files</p>
                        <div className="flex gap-3">
                          <span className="bg-slate-100 text-slate-600 text-xs font-bold px-3 py-1.5 rounded-md">PDF</span>
                          <span className="bg-slate-100 text-slate-600 text-xs font-bold px-3 py-1.5 rounded-md">DOCX</span>
                          <span className="bg-slate-100 text-slate-600 text-xs font-bold px-3 py-1.5 rounded-md">TXT</span>
                        </div>
                      </>
                    )}
                  </div>
                </>
              )}

              {/* Manual Entry (shown when paste is selected) */}
              {inputMode === 'paste' && (
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="font-bold text-slate-900">Paste Lease Text</h3>
                    <span className="text-xs font-bold text-slate-400 bg-slate-100 px-2 py-1 rounded">MANUAL ENTRY</span>
                  </div>
                  <textarea
                    ref={leaseTextRef}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm text-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[200px]"
                    placeholder="Paste the legal text of your lease agreement here for a quick scan..."
                    defaultValue={`Property Address: 742 Evergreen Terrace, Apt 4B, Los Angeles, CA 90012\nMonthly Rent: $1,800/month\nSecurity Deposit: 2-month security deposit\nSubletting: No subletting allowed\nEarly Termination Fee: $500\nPet Policy: No pets permitted\nLandlord Entry Notice: 12-hour notice required\nAnnual Rent Increase: Up to 10% annually\nTenant Repair Responsibility: All repairs under $200\nLease Auto-Renewal: Renews for 12 months if not cancelled 90 days before expiry`}
                  ></textarea>
                </div>
              )}

              {/* City Name & Landlord Email */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                  <label className="block font-bold text-slate-900 text-sm mb-2">City Name</label>
                  <input
                    ref={cityRef}
                    type="text"
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-sm text-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g. San Francisco"
                    defaultValue="California"
                  />
                </div>
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                  <label className="block font-bold text-slate-900 text-sm mb-2">Landlord Email</label>
                  <input
                    ref={emailRef}
                    type="email"
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-sm text-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g. landlord@example.com"
                    defaultValue="phurpawangchuk20@gmail.com"
                  />
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 flex items-center gap-2">
                  <AlertCircle className="text-rose-600 shrink-0" size={18} />
                  <p className="text-sm text-rose-700 font-medium">{error}</p>
                </div>
              )}

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
                  onClick={handleAnalyze}
                  disabled={analysisLoading}
                  className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition-colors shadow-md flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
                >
                  {analysisLoading ? (
                    <div className="flex flex-col items-center gap-1">
                      <div className="flex items-center gap-2">
                        <Loader2 size={18} className="animate-spin" />
                        <span>Analyzing...</span>
                      </div>
                      <span className="text-xs text-blue-200 font-medium">
                        Agent: {AGENT_STEPS[agentStep]}
                      </span>
                    </div>
                  ) : (
                    <>
                      Analyze Lease <ArrowRight size={18} />
                    </>
                  )}
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
