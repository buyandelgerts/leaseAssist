type NavbarView =
  | 'home'
  | 'search'
  | 'detail'
  | 'analysis-upload'
  | 'analysis-result'
  | 'calculator';

interface NavbarProps {
  currentView: NavbarView;
  setCurrentView: (view: NavbarView) => void;
}

const Navbar = ({ currentView, setCurrentView }: NavbarProps) => (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center gap-8">
            <div 
              className="text-xl font-bold text-slate-900 cursor-pointer flex items-center gap-2"
              onClick={() => setCurrentView('home')}
            >
              Lease Assist
            </div>
            <div className="hidden md:flex space-x-6 text-sm font-medium text-slate-500">
              <button 
                onClick={() => setCurrentView('search')}
                className={`hover:text-blue-600 transition-colors ${currentView === 'search' ? 'text-blue-600 border-b-2 border-blue-600 py-5' : 'py-5 border-b-2 border-transparent'}`}
              >
                Search
              </button>
              <button 
                onClick={() => setCurrentView('analysis-upload')}
                className={`hover:text-blue-600 transition-colors ${currentView.includes('analysis') ? 'text-blue-600 border-b-2 border-blue-600 py-5' : 'py-5 border-b-2 border-transparent'}`}
              >
                Analysis
              </button>
              <button 
                onClick={() => setCurrentView('calculator')}
                className={`hover:text-blue-600 transition-colors ${currentView === 'calculator' ? 'text-blue-600 border-b-2 border-blue-600 py-5' : 'py-5 border-b-2 border-transparent'}`}
              >
                Calculator
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
export default Navbar;  