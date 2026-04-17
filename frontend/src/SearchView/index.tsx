import { Map, Search, ChevronDown, BedDouble, Bath, Building, Dog } from "lucide-react";
import { PROPERTIES } from "../mockData";

type SearchViewRoute =
  | 'home'
  | 'search'
  | 'detail'
  | 'analysis-upload'
  | 'analysis-result'
  | 'calculator';

interface SearchViewProps {
  setCurrentView: (view: SearchViewRoute) => void;
}

const SearchView = ({ setCurrentView }: SearchViewProps) => {
    return (
      <div className="flex flex-col md:flex-row min-h-[calc(100vh-64px)] bg-slate-50">
        {/* Main Content */}
        <div className="flex-1 p-4 md:p-8 overflow-y-auto">
          {/* Top Search Bar & Filters */}
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 mb-8">
            <div className="flex flex-col lg:flex-row gap-4 mb-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-3 text-slate-400" size={20} />
                <input 
                  type="text" 
                  placeholder="Search by neighborhood or building name..." 
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-100 border-transparent rounded-lg focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
                  defaultValue="Manhattan, NY"
                />
              </div>
              <div className="flex gap-4">
                <select title="city" className="bg-slate-100 border-transparent rounded-lg px-4 py-2.5 text-slate-700 focus:ring-2 focus:ring-blue-200 min-w-[140px]">
                  <option>New York</option>
                  <option>California</option>
                </select>
                <input type="text" placeholder="Zipcode" className="bg-slate-100 border-transparent rounded-lg px-4 py-2.5 text-slate-700 focus:ring-2 focus:ring-blue-200 w-32" />
              </div>
            </div>
            
            <div className="flex flex-wrap items-center justify-between gap-4 border-t border-slate-100 pt-4">
              <div className="flex flex-wrap items-center gap-2">
                <div className="flex bg-slate-100 p-1 rounded-lg">
                  <button className="px-4 py-1.5 bg-blue-600 text-white rounded-md text-sm font-medium shadow-sm">Apartment</button>
                  <button className="px-4 py-1.5 text-slate-600 hover:bg-slate-200 rounded-md text-sm font-medium transition-colors">House</button>
                  <button className="px-4 py-1.5 text-slate-600 hover:bg-slate-200 rounded-md text-sm font-medium transition-colors">Condo</button>
                </div>
                <select title="bed" className="bg-slate-100 border-transparent rounded-lg px-3 py-2 text-sm text-slate-700">
                  <option>Bedrooms</option>
                  <option>1+</option>
                  <option>2+</option>
                </select>
                <select title="bath" className="bg-slate-100 border-transparent rounded-lg px-3 py-2 text-sm text-slate-700">
                  <option>Bathrooms</option>
                  <option>1+</option>
                </select>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-sm font-medium text-slate-700">Pet Allowed</span>
                <button title="pet" className="w-11 h-6 bg-slate-300 rounded-full relative transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                  <div className="w-4 h-4 bg-white rounded-full absolute left-1 top-1 shadow-sm transition-transform"></div>
                </button>
              </div>
            </div>
          </div>
  
          {/* Results Header */}
          <div className="flex justify-between items-end mb-6">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Available Residences</h1>
              <p className="text-slate-500 text-sm mt-1">248 results found in Manhattan, NY</p>
            </div>
            <div className="flex items-center gap-2 text-sm text-slate-600">
              Sort by
              <button className="font-semibold text-slate-900 flex items-center gap-1 hover:text-blue-600">
                Price: Low to High <ChevronDown size={16} />
              </button>
            </div>
          </div>
  
          {/* Property Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6 mb-10">
            {/* Main featured card */}
            <div 
              className="xl:col-span-2 bg-white rounded-2xl border border-slate-200 overflow-hidden hover:shadow-lg transition-all cursor-pointer group"
              onClick={() => setCurrentView('detail')}
            >
              <div className="relative h-72 overflow-hidden">
                <img src={PROPERTIES[0].image} alt={PROPERTIES[0].title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                <div className="absolute top-4 left-4 flex gap-2">
                  <span className="bg-emerald-400 text-emerald-950 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider shadow-sm">Verified Landlord</span>
                  <span className="bg-white/90 backdrop-blur-sm text-slate-800 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider shadow-sm">Available Now</span>
                </div>
              </div>
              <div className="p-6">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="text-2xl font-bold text-slate-900 mb-1 group-hover:text-blue-600 transition-colors">{PROPERTIES[0].title}</h3>
                    <p className="text-slate-500 flex items-center gap-1"><Map size={14} /> {PROPERTIES[0].location}</p>
                  </div>
                  <div className="text-right">
                    <span className="text-3xl font-bold text-blue-600">${PROPERTIES[0].price.toLocaleString()}</span>
                    <span className="text-slate-500 text-sm">/mo</span>
                  </div>
                </div>
                <div className="flex items-center gap-6 mt-6 pt-4 border-t border-slate-100 text-slate-700">
                  <span className="flex items-center gap-2 font-medium"><BedDouble size={18} className="text-slate-400" /> {PROPERTIES[0].beds} Bed</span>
                  <span className="flex items-center gap-2 font-medium"><Bath size={18} className="text-slate-400" /> {PROPERTIES[0].baths} Bath</span>
                  <span className="flex items-center gap-2 font-medium"><Building size={18} className="text-slate-400" /> {PROPERTIES[0].sqft} sq ft</span>
                  <span className="flex items-center gap-2 font-medium"><Dog size={18} className="text-slate-400" /> Pet Friendly</span>
                </div>
              </div>
            </div>
  
            {/* Other cards */}
            {PROPERTIES.slice(1).map((prop) => (
              <div 
                key={prop.id} 
                className="bg-white rounded-2xl border border-slate-200 overflow-hidden hover:shadow-lg transition-all cursor-pointer group flex flex-col"
                onClick={() => setCurrentView('detail')}
              >
                <div className="relative h-56 overflow-hidden">
                  <img src={prop.image} alt={prop.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                  <div className="absolute top-4 left-4 flex gap-2">
                    {prop.tags.map(tag => (
                      <span key={tag} className={`text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider shadow-sm ${
                        tag === 'NO PARKING' ? 'bg-red-500 text-white' : 
                        tag === 'PRICE CUT' ? 'bg-amber-100 text-amber-800' :
                        'bg-white/90 backdrop-blur-sm text-slate-800'
                      }`}>
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="p-5 flex-grow flex flex-col justify-between">
                  <div>
                    <div className="mb-2">
                       <span className="text-2xl font-bold text-blue-600">${prop.price.toLocaleString()}</span>
                       <span className="text-slate-500 text-sm">/mo</span>
                    </div>
                    <h3 className="text-lg font-bold text-slate-900 group-hover:text-blue-600 transition-colors line-clamp-1">{prop.title}</h3>
                    <p className="text-slate-500 text-sm flex items-center gap-1 mt-1 line-clamp-1"><Map size={14} /> {prop.location}</p>
                  </div>
                  <div className="flex items-center justify-between mt-4 pt-4 border-t border-slate-100">
                    <div className="flex gap-4 text-slate-700">
                      <span className="flex items-center gap-1.5 text-sm font-medium"><BedDouble size={16} className="text-slate-400"/> {prop.beds}</span>
                      <span className="flex items-center gap-1.5 text-sm font-medium"><Bath size={16} className="text-slate-400"/> {prop.baths}</span>
                    </div>
                    <span className="text-xs text-slate-400 font-medium">Listed 2 days ago</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
  
          <div className="flex justify-center">
            <button className="bg-slate-200 text-slate-700 hover:bg-slate-300 px-8 py-3 rounded-lg font-medium transition-colors">
              Load More Results
            </button>
          </div>
        </div>
      </div>
    );
  };

  export default SearchView;