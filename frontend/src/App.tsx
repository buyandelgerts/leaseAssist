import { useState } from "react";
import Navbar from "./Navbar";
import HomeView from "./HomeView";
import SearchView from "./SearchView";
import PropertyDetailView from "./PropertyDetailView";
import AnalysisUploadView from "./AnalysisUploadView";
import AnalysisResultView from "./AnalysisResultView";
import CalculatorView from "./CalculatorView";
import Footer from "./Footer";
import ChatbotOverlay from "./ChatbotOverlay";
import { MessageCircle } from "lucide-react";

type AppView =
  | "home"
  | "search"
  | "detail"
  | "analysis-upload"
  | "analysis-result"
  | "calculator";

export interface SelectedProperty {
  id: string | number;
  title: string;
  location: string;
  price: number;
  beds: number;
  baths: number;
  sqft: number;
  image: string;
  summary: string;
}

export default function App() {
  const [currentView, setCurrentView] = useState<AppView>("home");
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [analysisResult, setAnalysisResult] = useState("");
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [eligibilityResult, setEligibilityResult] = useState("");
  const [selectedProperty, setSelectedProperty] = useState<SelectedProperty | null>(null);

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 flex flex-col">
      <Navbar currentView={currentView} setCurrentView={setCurrentView} />

      <main className="grow w-full max-w-7xl mx-auto">
        {currentView === 'home' && <HomeView setCurrentView={setCurrentView} />}
        {currentView === 'search' && (
          <SearchView
            setCurrentView={setCurrentView}
            setSelectedProperty={setSelectedProperty}
          />
        )}
        {currentView === 'detail' && (
          <PropertyDetailView
            setCurrentView={setCurrentView}
            selectedProperty={selectedProperty}
          />
        )}
        {currentView === 'analysis-upload' && (
          <AnalysisUploadView
            setCurrentView={setCurrentView}
            setAnalysisResult={setAnalysisResult}
            analysisLoading={analysisLoading}
            setAnalysisLoading={setAnalysisLoading}
          />
        )}
        {currentView === 'analysis-result' && (
          <AnalysisResultView
            setCurrentView={setCurrentView}
            analysisResult={analysisResult}
          />
        )}
        {currentView === 'calculator' && (
          <CalculatorView setEligibilityResult={setEligibilityResult} />
        )}
      </main>

      <Footer />

      <ChatbotOverlay
        isOpen={isChatOpen}
        setIsOpen={setIsChatOpen}
        setCurrentView={setCurrentView}
        sessionContext={{
          eligibility_result: eligibilityResult || undefined,
          lease_analysis: analysisResult || undefined,
        }}
      />

      {/* Floating Action Button for Chatbot */}
      {!isChatOpen && (
        <button title="chat"
          onClick={() => setIsChatOpen(true)}
          className="fixed bottom-6 right-6 p-4 bg-blue-600 text-white rounded-full shadow-xl hover:bg-blue-700 transition-all z-50 group"
        >
          <MessageCircle size={28} className="group-hover:scale-110 transition-transform" />
          <div className="absolute top-0 right-0 w-3 h-3 bg-green-400 rounded-full border-2 border-white"></div>
        </button>
      )}
    </div>
  );
}
