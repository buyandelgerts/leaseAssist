import { Activity, AlertCircle, CheckCircle, ChevronDown, FileText, Percent, Shield, Zap } from "lucide-react";

type HomeViewRoute =
  | 'home'
  | 'search'
  | 'detail'
  | 'analysis-upload'
  | 'analysis-result'
  | 'calculator';

interface HomeViewProps {
  setCurrentView: (view: HomeViewRoute) => void;
}

const HomeView = ({ setCurrentView }: HomeViewProps) => (
    <div className="w-full pb-16">
      {/* Hero Section */}
      <div className="relative w-full h-[400px] bg-slate-900 overflow-hidden">
        <img 
          src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80" 
          alt="Modern Home Architecture" 
          className="absolute inset-0 w-full h-full object-cover opacity-50"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-50 via-transparent to-slate-900/40"></div>
        
        <div className="relative h-full flex flex-col items-center justify-center px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4 tracking-tight">
            Find Your <span className="text-blue-300">Perspective.</span>
          </h1>
          <p className="text-lg md:text-xl text-slate-200 mb-12 max-w-2xl font-light">
            A curated selection of architectural residences, simplified for the discerning tenant.
          </p>
        </div>
      </div>
  
      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="mb-12 flex flex-col md:flex-row justify-between items-end gap-6">
          <div>
            <h3 className="text-sm font-bold text-blue-600 tracking-widest uppercase mb-2">The Advantage</h3>
            <h2 className="text-4xl font-bold text-slate-900 tracking-tight">Curation as a Service.</h2>
          </div>
          <p className="text-slate-500 max-w-md text-lg">
            We skip the standard lists to bring you spaces that resonate with modern architectural principles.
          </p>
        </div>
  
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Large Feature Card */}
          <div className="md:col-span-1 bg-white rounded-2xl p-8 border border-slate-100 shadow-sm relative overflow-hidden flex flex-col h-[400px]">
            <div className="w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center mb-6">
              <CheckCircle size={24} />
            </div>
            <h3 className="text-2xl font-bold text-slate-900 mb-4">Verified Landlords</h3>
            <p className="text-slate-600 flex-grow">
              Every property undergoes a 42-point architectural and legal inspection before being listed on Aura.
            </p>
            <div className="flex items-center gap-3 mt-4">
              <span className="bg-green-50 text-green-700 text-xs font-bold px-3 py-1 rounded-full">98% Satisfaction</span>
              <button className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">Read Member Stories</button>
            </div>
            <div className="absolute -bottom-20 -right-20 w-64 h-64 bg-green-50 rounded-full blur-3xl opacity-50 pointer-events-none"></div>
          </div>
  
          {/* Feature Column */}
          <div className="md:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-6 h-[400px]">
            {/* Image Card */}
            <div className="sm:col-span-2 bg-slate-900 rounded-2xl relative overflow-hidden h-48 group cursor-pointer" onClick={() => setCurrentView('detail')}>
              <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Penthouse" className="absolute inset-0 w-full h-full object-cover opacity-60 group-hover:opacity-80 transition-opacity duration-500" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
              <div className="absolute bottom-6 left-6">
                <span className="text-xs font-bold tracking-wider text-white/70 uppercase mb-1 block">New on the Market</span>
                <h4 className="text-xl font-bold text-white">The Obsidian Penthouse</h4>
                <p className="text-white/80 text-sm">Downtown District • $12,400/mo</p>
              </div>
            </div>
            
            {/* Small Cards */}
            <div 
              className="bg-blue-600 rounded-2xl p-6 text-white cursor-pointer hover:bg-blue-700 transition-colors relative overflow-hidden group"
              onClick={() => setCurrentView('analysis-upload')}
            >
              <div className="absolute top-0 right-0 p-6 opacity-20 transform translate-x-4 -translate-y-4 group-hover:translate-x-2 group-hover:-translate-y-2 transition-transform">
                <Activity size={80} />
              </div>
              <Activity className="mb-4" size={24} />
              <h4 className="text-lg font-bold mb-2">Deep Analysis</h4>
              <p className="text-blue-100 text-sm opacity-90">Market trend data for every zip code.</p>
            </div>
            
            <div 
              className="bg-slate-100 rounded-2xl p-6 border border-slate-200 cursor-pointer hover:bg-slate-200 transition-colors group"
              onClick={() => setCurrentView('calculator')}
            >
              <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center text-blue-600 mb-4 shadow-sm">
                <Percent size={20} />
              </div>
              <h4 className="text-lg font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors">Lease Calculator</h4>
              <p className="text-slate-500 text-sm">Calculate utilities and hidden costs instantly.</p>
            </div>
          </div>
        </div>
      </div>
  
      {/* Transparency Banner */}
      <div className="bg-white border-y border-slate-200 py-16 text-center">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-slate-900 mb-4">Total Transparency</h2>
          <p className="text-slate-500 mb-8 max-w-2xl mx-auto">
            We highlight what others hide. Professional stamps for every listing ensuring you know exactly what you're stepping into.
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            <span className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-green-50 text-green-700 text-sm font-medium border border-green-100">
              <Shield size={16} /> Verified Landlord
            </span>
            <span className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-emerald-50 text-emerald-700 text-sm font-medium border border-emerald-100">
              <Zap size={16} /> Low Energy Cost
            </span>
            <span className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-rose-50 text-rose-700 text-sm font-medium border border-rose-100">
              <AlertCircle size={16} /> Street Noise: Moderate
            </span>
            <span className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-red-50 text-red-700 text-sm font-medium border border-red-100">
              <FileText size={16} /> No On-site Parking
            </span>
          </div>
        </div>
      </div>
    </div>
  );

  export default HomeView;