import { ChevronDown, Check, Zap, AlertCircle } from "lucide-react";

const CalculatorView = () => {
    return (
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-slate-900 mb-4">Eligibility Calculator</h1>
          <p className="text-lg text-slate-600 max-w-2xl">
            Our architectural leasing model prioritizes financial transparency. Input your details to receive an instant assessment of your leasing potential.
          </p>
        </div>
  
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          
          {/* Left Column - Forms & Image */}
          <div className="space-y-8">
            <div className="bg-slate-50 border border-slate-200 rounded-2xl p-8">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
                <div>
                  <label htmlFor="monthly-income" className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">Monthly Income</label>
                  <div className="relative">
                    <span className="absolute left-4 top-3 text-slate-500 font-medium">$</span>
                    <input id="monthly-income" type="text" defaultValue="5,000" className="w-full bg-white border border-slate-200 rounded-xl py-3 pl-8 pr-4 text-slate-900 font-semibold focus:ring-2 focus:ring-blue-500 outline-none" />
                  </div>
                </div>
                <div>
                  <label htmlFor="credit-score" className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">Credit Score</label>
                  <input id="credit-score" type="text" defaultValue="720" className="w-full bg-white border border-slate-200 rounded-xl py-3 px-4 text-slate-900 font-semibold focus:ring-2 focus:ring-blue-500 outline-none" />
                </div>
                <div>
                  <label htmlFor="employment-status" className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">Employment Status</label>
                  <div className="relative">
                    <select id="employment-status" title="Employment status" className="w-full appearance-none bg-white border border-slate-200 rounded-xl py-3 px-4 text-slate-900 font-medium focus:ring-2 focus:ring-blue-500 outline-none">
                      <option>Full-time Professional</option>
                      <option>Freelance / Contractor</option>
                      <option>Business Owner</option>
                    </select>
                    <ChevronDown className="absolute right-4 top-3.5 text-slate-400" size={18} />
                  </div>
                </div>
                <div>
                  <label htmlFor="monthly-debt" className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">Total Monthly Debt</label>
                  <div className="relative">
                    <span className="absolute left-4 top-3 text-slate-500 font-medium">$</span>
                    <input id="monthly-debt" type="text" defaultValue="400" className="w-full bg-white border border-slate-200 rounded-xl py-3 pl-8 pr-4 text-slate-900 font-semibold focus:ring-2 focus:ring-blue-500 outline-none" />
                  </div>
                </div>
              </div>
              <button className="bg-blue-600 text-white px-8 py-3.5 rounded-xl font-bold hover:bg-blue-700 transition-colors shadow-md">
                Assess Eligibility
              </button>
            </div>
  
            <div className="rounded-2xl overflow-hidden relative h-64">
              <img src="https://images.unsplash.com/photo-1497366216548-37526070297c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80" alt="Office space" className="w-full h-full object-cover" />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/40 to-transparent"></div>
              <div className="absolute bottom-6 left-6 right-6">
                <h3 className="text-2xl font-bold text-white mb-2">Secure Your Future Space</h3>
                <p className="text-slate-200">Our underwriting process is built on your potential, not just arbitrary numbers.</p>
              </div>
            </div>
          </div>
  
          {/* Right Column - Results */}
          <div className="space-y-8">
            
            {/* Main Chart Card */}
            <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm">
              <div className="flex justify-between items-center mb-10">
                <h3 className="text-sm font-bold text-slate-500 tracking-widest uppercase">Likelihood of Eligibility</h3>
                <span className="bg-green-100 text-green-700 text-xs font-bold px-3 py-1 rounded-full flex items-center gap-1.5 border border-green-200">
                  <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></div>
                  LIVE ANALYSIS
                </span>
              </div>
  
              <div className="flex justify-center mb-10">
                {/* CSS Donut Chart Trick */}
                <div 
                  className="relative w-64 h-64 rounded-full flex items-center justify-center transition-all duration-1000" 
                  style={{ background: 'conic-gradient(#0056D2 78%, #e2e8f0 0)' }}
                >
                  <div className="absolute inset-4 rounded-full bg-white flex flex-col items-center justify-center shadow-[inset_0_2px_10px_rgba(0,0,0,0.05)]">
                    <span className="text-5xl font-bold text-slate-900 mb-1">High</span>
                    <span className="text-lg font-medium text-slate-500">78% Match</span>
                  </div>
                </div>
              </div>
  
              <div className="space-y-4 pt-6 border-t border-slate-100">
                <div className="flex justify-between items-center">
                  <span className="text-slate-600 font-medium">Debt-to-Income Ratio</span>
                  <span className="font-bold text-green-600">Optimal</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600 font-medium">Credit Health</span>
                  <span className="font-bold text-blue-600">Strong</span>
                </div>
              </div>
            </div>
  
            {/* Path to Approval */}
            <div>
              <h3 className="text-sm font-bold text-slate-500 tracking-widest uppercase mb-4">Path to Approval</h3>
              
              <div className="space-y-4">
                <div className="bg-green-50 border border-green-200 rounded-xl p-5 flex gap-4">
                  <div className="w-10 h-10 bg-green-500 text-white rounded-full flex items-center justify-center shrink-0">
                    <Check size={20} />
                  </div>
                  <div>
                    <h4 className="font-bold text-green-900 mb-1">Verified Stability</h4>
                    <p className="text-sm text-green-800/80">Your employment tenure at 2+ years serves as a significant green flag for our underwriters.</p>
                  </div>
                </div>
  
                <div className="bg-slate-100 border border-slate-200 rounded-xl p-5 flex gap-4">
                  <div className="w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center shrink-0">
                    <Zap size={20} />
                  </div>
                  <div>
                    <h4 className="font-bold text-slate-900 mb-1">Improve Your Leverage</h4>
                    <p className="text-sm text-slate-600">Reducing monthly revolving debt below $250 could elevate your eligibility to the "Premium" tier.</p>
                  </div>
                </div>
  
                <div className="bg-rose-50 border border-rose-200 rounded-xl p-5 flex gap-4">
                  <div className="w-10 h-10 bg-rose-500 text-white rounded-full flex items-center justify-center shrink-0">
                    <AlertCircle size={20} />
                  </div>
                  <div>
                    <h4 className="font-bold text-rose-900 mb-1">Documentation Notice</h4>
                    <p className="text-sm text-rose-800/80">If transitioning to freelance status, requires 6 months of bank statements to verify income consistency.</p>
                  </div>
                </div>
              </div>
            </div>
  
          </div>
        </div>
      </div>
    );
  };

  export default CalculatorView;