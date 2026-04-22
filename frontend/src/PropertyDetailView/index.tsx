import { useState } from "react";
import { Map, ArrowRight, Settings, Zap, Activity, Shield, Dog, CheckCircle, AlertCircle, MessageCircle, Loader2 } from "lucide-react";
import type { SelectedProperty } from "../App";

type PropertyDetailRoute =
  | 'home'
  | 'search'
  | 'detail'
  | 'analysis-upload'
  | 'analysis-result'
  | 'calculator';

interface PropertyDetailViewProps {
  setCurrentView: (view: PropertyDetailRoute) => void;
  selectedProperty: SelectedProperty | null;
}

interface TourRequestResponse {
  status: string;
  process: string;
  result?: string;
  detail?: string;
}

const API_BASE = import.meta.env.VITE_API_URL;
const DEFAULT_LANDLORD_EMAIL = import.meta.env.VITE_LANDLORD_EMAIL;

const PropertyDetailView = ({ setCurrentView, selectedProperty }: PropertyDetailViewProps) => {
    const propertyTitle = selectedProperty?.title || "The Meridian Loft";
    const propertyLocation = selectedProperty?.location || "450 Architecture Way, Design District, San Francisco";
    const propertyPrice = selectedProperty?.price ?? 4850;
    const propertySqft = selectedProperty?.sqft ?? 1240;
    const propertySummary = selectedProperty?.summary;
    const [preferredDate, setPreferredDate] = useState("");
    const [preferredTime, setPreferredTime] = useState("09:00 AM");
    const [tenantPhone, setTenantPhone] = useState("");
    const [isScheduling, setIsScheduling] = useState(false);
    const [tourError, setTourError] = useState("");
    const [tourSuccess, setTourSuccess] = useState("");
    const mainImage =
      selectedProperty?.image ||
      "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80";

    const handleScheduleTour = async () => {
      setTourError("");
      setTourSuccess("");

      if (!preferredDate) {
        setTourError("Please select a preferred date.");
        return;
      }

      const payload = {
        landlord_email: DEFAULT_LANDLORD_EMAIL,
        tenant_name: "Website Visitor",
        property_address: propertyLocation,
        preferred_date: preferredDate,
        preferred_time: preferredTime,
        tenant_phone: tenantPhone.trim() || undefined,
      };

      setIsScheduling(true);
      try {
        const response = await fetch(`${API_BASE}/tour-request`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const data = (await response.json()) as TourRequestResponse;
        if (!response.ok) {
          throw new Error(data?.detail || "Tour request failed.");
        }

        const apiResultText = data?.result || "Tour request sent successfully.";
        setTourSuccess(apiResultText);
      } catch (error) {
        const message =
          error instanceof Error ? error.message : "Something went wrong while scheduling the tour.";
        setTourError(message);
      } finally {
        setIsScheduling(false);
      }
    };

    return (
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Back & Breadcrumb */}
        <button 
          onClick={() => setCurrentView('search')}
          className="flex items-center gap-2 text-sm text-slate-500 hover:text-blue-600 mb-6 transition-colors"
        >
          <ArrowRight className="rotate-180" size={16} /> Back to Search
        </button>
  
        {/* Hero Image Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8 h-[500px]">
          <div className="md:col-span-2 h-full rounded-2xl overflow-hidden relative group">
            <img src={mainImage} alt={propertyTitle} className="w-full h-full object-cover" />
            <div className="absolute inset-0 bg-blue-900/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
              <h2 className="text-white text-3xl font-bold tracking-widest uppercase">Primary Living Area</h2>
            </div>
          </div>
          <div className="md:col-span-2 grid grid-rows-2 gap-4 h-full">
            <div className="rounded-2xl overflow-hidden">
              <img src="https://images.unsplash.com/photo-1556912172-45b7ee8819d3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Kitchen" className="w-full h-full object-cover" />
            </div>
            <div className="grid grid-cols-2 gap-4">
               <div className="rounded-2xl overflow-hidden">
                 <img src="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Bedroom" className="w-full h-full object-cover" />
               </div>
               <div className="rounded-2xl overflow-hidden relative group cursor-pointer">
                 <img src="https://images.unsplash.com/photo-1505691938895-1758d7feb511?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Dining" className="w-full h-full object-cover" />
                 <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                    <span className="text-white font-medium">+12 More Photos</span>
                 </div>
               </div>
            </div>
          </div>
        </div>
  
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Main Content Column */}
          <div className="lg:col-span-2">
            <div className="mb-8">
              <div className="flex items-center gap-3 mb-4">
                <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-3 py-1 rounded-full">AVAILABLE NOW</span>
                <span className="text-slate-500 text-sm font-medium">Ref ID: {selectedProperty?.id ?? "AL-4802"}</span>
              </div>
              <h1 className="text-4xl font-bold text-slate-900 mb-2">{propertyTitle}</h1>
              <p className="text-lg text-slate-600 flex items-center gap-2"><Map size={18} /> {propertyLocation}</p>
            </div>
  
            <div className="flex gap-8 mb-10 pb-8 border-b border-slate-200">
              <div>
                <div className="flex items-baseline text-blue-600">
                  <span className="text-4xl font-bold">${propertyPrice.toLocaleString()}</span>
                  <span className="text-lg font-medium">/mo</span>
                </div>
                <span className="text-xs font-bold text-slate-500 tracking-wider uppercase">Monthly Lease</span>
              </div>
              <div className="w-px bg-slate-200"></div>
              <div>
                <div className="flex items-baseline text-slate-900">
                  <span className="text-4xl font-bold">{propertySqft.toLocaleString()}</span>
                  <span className="text-lg font-medium ml-1">sq ft</span>
                </div>
                <span className="text-xs font-bold text-slate-500 tracking-wider uppercase">Total Space</span>
              </div>
            </div>
  
            <div className="mb-10">
              <h3 className="text-2xl font-bold text-slate-900 mb-4">Architectural Narrative</h3>
              <p className="text-slate-600 leading-relaxed">
                {propertySummary || "Designed with an uncompromising vision of modern living, The Meridian Loft offers a curated experience in the heart of the Design District. Featuring expansive 14-foot ceilings and raw industrial elements softened by white oak finishes, this space transitions seamlessly from a high-performance workspace to an intimate sanctuary. The open-plan layout is anchored by a chef-inspired kitchen and floor-to-ceiling glass that frames the urban landscape as living art."}
              </p>
            </div>
  
            <div className="mb-10">
              <h3 className="text-2xl font-bold text-slate-900 mb-6">Premium Amenities</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="bg-slate-50 p-5 rounded-xl border border-slate-100">
                  <Settings className="text-blue-600 mb-3" size={24} />
                  <h4 className="font-bold text-slate-900 mb-1">HVAC Control</h4>
                  <p className="text-sm text-slate-500">Smart multi-zone climate management</p>
                </div>
                <div className="bg-slate-50 p-5 rounded-xl border border-slate-100">
                  <Zap className="text-blue-600 mb-3" size={24} />
                  <h4 className="font-bold text-slate-900 mb-1">EV Parking</h4>
                  <p className="text-sm text-slate-500">Reserved subterranean spot with Tesla charging</p>
                </div>
                <div className="bg-slate-50 p-5 rounded-xl border border-slate-100">
                  <Activity className="text-blue-600 mb-3" size={24} />
                  <h4 className="font-bold text-slate-900 mb-1">Wellness Hub</h4>
                  <p className="text-sm text-slate-500">24/7 Peloton-equipped fitness center</p>
                </div>
                <div className="bg-slate-50 p-5 rounded-xl border border-slate-100">
                  <Shield className="text-blue-600 mb-3" size={24} />
                  <h4 className="font-bold text-slate-900 mb-1">Concierge</h4>
                  <p className="text-sm text-slate-500">On-site valet and package management</p>
                </div>
              </div>
            </div>
  
            {/* Pet Policy */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-12 h-12 bg-green-100 text-green-600 rounded-xl flex items-center justify-center">
                  <Dog size={24} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900">Pet Policy</h3>
                  <p className="text-sm text-slate-500">We welcome your architectural companions.</p>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="flex gap-3">
                  <CheckCircle className="text-green-500 shrink-0 mt-0.5" size={18} />
                  <div>
                    <h5 className="font-semibold text-slate-900 text-sm">Cats & Dogs Allowed</h5>
                    <p className="text-xs text-slate-500 mt-1">Up to two pets per residence</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <AlertCircle className="text-rose-500 shrink-0 mt-0.5" size={18} />
                  <div>
                    <h5 className="font-semibold text-slate-900 text-sm">Breed Restrictions</h5>
                    <p className="text-xs text-slate-500 mt-1">Standard restricted breeds apply</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <CheckCircle className="text-green-500 shrink-0 mt-0.5" size={18} />
                  <div>
                    <h5 className="font-semibold text-slate-900 text-sm">Pet Park Access</h5>
                    <p className="text-xs text-slate-500 mt-1">Access to the private 4th-floor pet lounge</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <AlertCircle className="text-amber-500 shrink-0 mt-0.5" size={18} />
                  <div>
                    <h5 className="font-semibold text-slate-900 text-sm">Pet Deposit</h5>
                    <p className="text-xs text-slate-500 mt-1">$500 one-time fee per pet</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          {/* Sticky Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-24 space-y-6">
              
              {/* Action Card */}
              <div className="bg-white rounded-2xl border border-slate-200 shadow-lg p-6">
                <h3 className="text-xl font-bold text-slate-900 mb-6">Request a Tour</h3>
                
                <div className="space-y-4 mb-6">
                  <div>
                    <label className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">Preferred Date</label>
                    <div className="relative">
                      <input
                        title="date"
                        type="date"
                        value={preferredDate}
                        onChange={(event) => setPreferredDate(event.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 rounded-lg py-3 px-4 text-slate-700 focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">Preferred Time</label>
                    <select
                      title="clock"
                      value={preferredTime}
                      onChange={(event) => setPreferredTime(event.target.value)}
                      className="w-full bg-slate-50 border border-slate-200 rounded-lg py-3 px-4 text-slate-700 focus:ring-2 focus:ring-blue-500 appearance-none"
                    >
                      <option>09:00 AM</option>
                      <option>10:00 AM</option>
                      <option>01:00 PM</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-wider">Phone Number</label>
                    <input
                      title="tenant-phone"
                      type="tel"
                      value={tenantPhone}
                      onChange={(event) => setTenantPhone(event.target.value)}
                      placeholder="(555) 123-4567"
                      className="w-full bg-slate-50 border border-slate-200 rounded-lg py-3 px-4 text-slate-700 focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
                
                <button
                  type="button"
                  onClick={handleScheduleTour}
                  disabled={isScheduling}
                  className="w-full bg-blue-600 text-white py-3.5 rounded-xl font-bold hover:bg-blue-700 transition-colors shadow-md shadow-blue-600/20 mb-4 disabled:bg-blue-300 disabled:cursor-not-allowed inline-flex items-center justify-center gap-2"
                >
                  {isScheduling && <Loader2 size={18} className="animate-spin" />}
                  {isScheduling ? "Scheduling..." : "Schedule Tour"}
                </button>
                {tourError && <p className="text-sm text-rose-600 mb-4">{tourError}</p>}
                {tourSuccess && <p className="text-sm text-emerald-700 mb-4">{tourSuccess}</p>}
  
                <div className="pt-6 border-t border-slate-100">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="relative">
                      <div className="w-12 h-12 rounded-full bg-slate-200 overflow-hidden">
                        <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80" alt="Agent" />
                      </div>
                      <div className="absolute bottom-0 right-0 w-3.5 h-3.5 bg-green-500 border-2 border-white rounded-full"></div>
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-900 text-sm">Sarah Mitchell</h4>
                      <p className="text-xs text-slate-500">Senior Leasing Executive</p>
                    </div>
                  </div>
                  <div className="bg-slate-100 p-3 rounded-lg mb-4 text-sm text-slate-600">
                    "I'm interested in the Meridian Loft. Could you provide details on parking availability?"
                  </div>
                  <button className="w-full bg-white border border-slate-300 text-slate-700 py-2.5 rounded-lg font-medium hover:bg-slate-50 transition-colors flex justify-center items-center gap-2">
                    <MessageCircle size={18} /> Message Agent
                  </button>
                </div>
              </div>
  
              {/* Map Mini-Card */}
              <div className="bg-slate-100 rounded-2xl overflow-hidden h-48 relative border border-slate-200">
                <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
                {/* Abstract map representation */}
                <div className="w-full h-full flex items-center justify-center text-slate-400">
                  [ Map Area Placeholder ]
                </div>
                <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm px-3 py-1.5 rounded-md shadow-sm">
                  <span className="text-xs font-bold text-slate-900">VIEW AREA MAP</span>
                </div>
                <div className="absolute bottom-0 left-0 right-0 bg-white p-4">
                  <h5 className="font-bold text-slate-900 text-sm">Walker's Paradise: 98</h5>
                  <p className="text-xs text-slate-500">San Francisco Design District</p>
                </div>
              </div>
  
            </div>
          </div>
        </div>
      </div>
    );
  };

  export default PropertyDetailView;