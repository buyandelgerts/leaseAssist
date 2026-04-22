import { useState } from "react";
import type { FormEvent } from "react";
import { ChevronDown, AlertCircle, Loader2 } from "lucide-react";

interface CalculatorViewProps {
  setEligibilityResult?: (result: string) => void;
}

interface EligibilityResult {
  is_eligible: boolean;
  confidence_score: number;
  reasons: string[];
  applied_rules: string[];
  recommendation: string;
}

const API_BASE = import.meta.env.VITE_API_URL;

const parseCurrencyInput = (value: string): number => {
  const cleaned = value.replace(/[^0-9.]/g, "");
  return Number(cleaned || "0");
};

const CalculatorView = ({ setEligibilityResult }: CalculatorViewProps) => {
    const [monthlyIncome, setMonthlyIncome] = useState("0");
    const [desiredBudget, setDesiredBudget] = useState("0");
    const [monthlyDebts, setMonthlyDebts] = useState("0");
    const [state, setState] = useState("IL");
    const [isLoading, setIsLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [apiResult, setApiResult] = useState<EligibilityResult | null>(null);

    const handleSubmit = async (event: FormEvent) => {
      event.preventDefault();
      setErrorMessage("");
      setApiResult(null);

      const payload = {
        monthly_income: parseCurrencyInput(monthlyIncome),
        monthly_debts: parseCurrencyInput(monthlyDebts),
        desired_budget: parseCurrencyInput(desiredBudget),
        state,
      };

      if (!payload.monthly_income || !payload.desired_budget) {
        setErrorMessage("Monthly income and desired budget are required.");
        return;
      }

      setIsLoading(true);
      try {
        const response = await fetch(`${API_BASE}/eligibility`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data?.detail || "Eligibility request failed.");
        }

        const resultObject = data?.result as EligibilityResult;
        setApiResult(resultObject);
        setEligibilityResult?.(JSON.stringify(resultObject, null, 2));
      } catch (error) {
        setErrorMessage(error instanceof Error ? error.message : "Something went wrong.");
      } finally {
        setIsLoading(false);
      }
    };

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
            <form onSubmit={handleSubmit} className="bg-slate-50 border border-slate-200 rounded-2xl p-8">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
                <div>
                  <label htmlFor="monthly-income" className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">Monthly Income</label>
                  <div className="relative">
                    <span className="absolute left-4 top-3 text-slate-500 font-medium">$</span>
                    <input
                      id="monthly-income"
                      type="text"
                      value={monthlyIncome}
                      onChange={(event) => setMonthlyIncome(event.target.value)}
                      className="w-full bg-white border border-slate-200 rounded-xl py-3 pl-8 pr-4 text-slate-900 font-semibold focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                  </div>
                </div>
                <div>
                  <label htmlFor="desired-budget" className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">Desired Budget</label>
                  <div className="relative">
                    <span className="absolute left-4 top-3 text-slate-500 font-medium">$</span>
                    <input
                      id="desired-budget"
                      type="text"
                      value={desiredBudget}
                      onChange={(event) => setDesiredBudget(event.target.value)}
                      className="w-full bg-white border border-slate-200 rounded-xl py-3 pl-8 pr-4 text-slate-900 font-semibold focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                  </div>
                </div>
                <div>
                  <label htmlFor="state" className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">State</label>
                  <div className="relative">
                    <select
                      id="state"
                      title="state"
                      value={state}
                      onChange={(event) => setState(event.target.value)}
                      className="w-full appearance-none bg-white border border-slate-200 rounded-xl py-3 px-4 text-slate-900 font-medium focus:ring-2 focus:ring-blue-500 outline-none"
                    >
                      <option value="IL">IL</option>
                      <option value="WA">WA</option>
                      <option value="NY">NY</option>
                      <option value="TX">TX</option>
                    </select>
                    <ChevronDown className="pointer-events-none absolute right-4 top-3.5 text-slate-400" size={18} />
                  </div>
                </div>
                <div>
                  <label htmlFor="monthly-debt" className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">Total Monthly Debt</label>
                  <div className="relative">
                    <span className="absolute left-4 top-3 text-slate-500 font-medium">$</span>
                    <input
                      id="monthly-debt"
                      type="text"
                      value={monthlyDebts}
                      onChange={(event) => setMonthlyDebts(event.target.value)}
                      className="w-full bg-white border border-slate-200 rounded-xl py-3 pl-8 pr-4 text-slate-900 font-semibold focus:ring-2 focus:ring-blue-500 outline-none"
                    />
                  </div>
                </div>
              </div>
              {errorMessage && <p className="text-sm text-rose-600 mb-4">{errorMessage}</p>}
              <button
                type="submit"
                disabled={isLoading}
                className="bg-blue-600 text-white px-8 py-3.5 rounded-xl font-bold hover:bg-blue-700 transition-colors shadow-md disabled:bg-blue-300 disabled:cursor-not-allowed inline-flex items-center gap-2"
              >
                {isLoading && <Loader2 size={18} className="animate-spin" />}
                {isLoading ? "Assessing..." : "Assess Eligibility"}
              </button>
            </form>
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

              {isLoading ? (
                <div className="py-16 flex flex-col items-center justify-center text-slate-600">
                  <Loader2 size={40} className="animate-spin text-blue-600 mb-4" />
                  <p className="font-medium">Running eligibility analysis...</p>
                </div>
              ) : !apiResult ? (
                <div className="py-16 text-center text-slate-500">
                  Submit your details to generate eligibility results.
                </div>
              ) : (
                <>
                  <div className="flex justify-center mb-10">
                    {/* CSS Donut Chart Trick */}
                    <div
                      className="relative w-64 h-64 rounded-full flex items-center justify-center transition-all duration-1000"
                      style={{
                        background: `conic-gradient(#0056D2 ${(apiResult.confidence_score ?? 0) * 100}%, #e2e8f0 0)`,
                      }}
                    >
                      <div className="absolute inset-4 rounded-full bg-white flex flex-col items-center justify-center shadow-[inset_0_2px_10px_rgba(0,0,0,0.05)]">
                        <span className="text-5xl font-bold text-slate-900 mb-1">
                          {apiResult.is_eligible ? "Eligible" : "Denied"}
                        </span>
                        <span className="text-lg font-medium text-slate-500">
                          {`${Math.round(apiResult.confidence_score * 100)}% Match`}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4 pt-6 border-t border-slate-100">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-600 font-medium">Debt-to-Income Ratio</span>
                      <span className={`font-bold ${apiResult.is_eligible ? "text-green-600" : "text-rose-600"}`}>
                        {apiResult.is_eligible ? "Within Range" : "Needs Improvement"}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-600 font-medium">Recommendation</span>
                      <span className="font-bold text-blue-600">
                        {apiResult.is_eligible ? "Approve" : "Deny"}
                      </span>
                    </div>
                  </div>
                </>
              )}
            </div>
  
            {/* Path to Approval */}
            <div>
              <h3 className="text-sm font-bold text-slate-500 tracking-widest uppercase mb-4">Path to Approval</h3>
              {apiResult && (
                <div className="mb-4 bg-gray-500 text-slate-100 rounded-xl p-4">
                  <h4 className="font-bold mb-2">Recommendation</h4>
                  <p className="text-sm mb-3">{apiResult.recommendation}</p>
                  <h5 className="font-semibold mb-2">Applied Rules</h5>
                  <div className="flex flex-wrap gap-2">
                    {apiResult.applied_rules.map((rule) => (
                      <span key={rule} className="text-xs px-2 py-1 rounded bg-slate-700">
                        {rule}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              
              <div className="space-y-4">
                {(apiResult?.reasons ?? []).map((reason, idx) => (
                  <div key={`${reason}-${idx}`} className="bg-rose-50 border border-rose-200 rounded-xl p-5 flex gap-4">
                    <div className="w-10 h-10 bg-rose-500 text-white rounded-full flex items-center justify-center shrink-0">
                      <AlertCircle size={20} />
                    </div>
                    <div>
                      <h4 className="font-bold text-rose-900 mb-1">Review Item</h4>
                      <p className="text-sm text-rose-800/80">{reason}</p>
                    </div>
                  </div>
                ))}
                {!apiResult && (
                  <div className="bg-slate-100 border border-slate-200 rounded-xl p-5">
                    <p className="text-sm text-slate-600">No results yet. Submit the form to see approval path details.</p>
                  </div>
                )}
              </div>
            </div>
  
          </div>
        </div>
      </div>
    );
  };

  export default CalculatorView;