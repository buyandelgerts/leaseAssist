import { useState } from "react";
import type { FormEvent } from "react";
import { Map, Search, ChevronDown, BedDouble, Bath, Loader2 } from "lucide-react";
import type { SelectedProperty } from "../App";

type SearchViewRoute =
  | 'home'
  | 'search'
  | 'detail'
  | 'analysis-upload'
  | 'analysis-result'
  | 'calculator';

interface SearchViewProps {
  setCurrentView: (view: SearchViewRoute) => void;
  setSelectedProperty: (property: SelectedProperty) => void;
}

interface SearchApiResponse {
  status: string;
  process: string;
  result?: {
    results?: Array<{
      id?: string | number;
      title?: string;
      formatted_address?: string;
      city?: string;
      state?: string;
      zip_code?: string;
      price?: number | string;
      beds?: number | string;
      baths?: number | string;
      sqft?: number | string;
      property_type?: string;
      content?: string;
      similarity_score?: number;
    }>;
  };
}

interface PropertyCard {
  id: string | number;
  title: string;
  address?: string;
  location: string;
  zip_code?: string;
  price: number;
  beds: number;
  baths: number;
  property_type?: string;
  sqft: number;
  image: string;
  tags: string[];
  summary: string;
}

const API_BASE = import.meta.env.VITE_API_URL;

const SearchView = ({ setCurrentView, setSelectedProperty }: SearchViewProps) => {
    const RESULTS_PAGE_SIZE = 6;
    const [cityState, setCityState] = useState("Chicago, IL");
    const [query, setQuery] = useState("");
    const [searchResult, setSearchResult] = useState<SearchApiResponse | null>(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [isSearching, setIsSearching] = useState(false);
    const [priceSortOrder, setPriceSortOrder] = useState<"asc" | "desc">("asc");
    const [visibleCount, setVisibleCount] = useState(RESULTS_PAGE_SIZE);
    const [hasSearched, setHasSearched] = useState(false);

    const city = cityState.split(",")[0]?.trim() ?? "";
    const state = cityState.split(",")[1]?.trim() ?? "";
    const apiResults = searchResult?.result?.results ?? [];
    const hasApiResults = apiResults.length > 0;

    const parseNumericValue = (value: unknown): number => {
      if (typeof value === "number") return value;
      if (typeof value !== "string") return NaN;
      const cleaned = value.replace(/[^0-9.-]/g, "");
      if (!cleaned) return NaN;
      return Number(cleaned);
    };

    const handleSearch = async (event: FormEvent) => {
      event.preventDefault();
      setErrorMessage("");
      setSearchResult(null);
      setVisibleCount(RESULTS_PAGE_SIZE);
      setHasSearched(true);

      if (!city || !state) {
        setErrorMessage("Please select a valid city and state.");
        return;
      }

      const payload: Record<string, string | number> = {
        city,
        state,
      };

      if (query.trim()) payload.query = query.trim();

      setIsSearching(true);
      try {
        const response = await fetch(`${API_BASE}/search`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data?.detail || "Search request failed.");
        }

        setSearchResult(data as SearchApiResponse);
      } catch (error) {
        const message =
          error instanceof Error ? error.message : "Something went wrong while searching.";
        setErrorMessage(message);
      } finally {
        setIsSearching(false);
      }
    };

    const cards: PropertyCard[] = hasApiResults
      ? apiResults.map((item, index) => {
          const parsedPrice = parseNumericValue(item.price);
          const parsedBeds = parseNumericValue(item.beds ?? (item as { bedrooms?: number | string }).bedrooms);
          const parsedBaths = parseNumericValue(item.baths ?? (item as { bathrooms?: number | string }).bathrooms);
          const parsedSqft = parseNumericValue(item.sqft ?? (item as { square_footage?: number | string }).square_footage);
          const cardLocation = [item.city, item.state].filter(Boolean).join(", ") || cityState;
        return {
            id: item.id ?? `api-${index}`,
            title: item.property_type || `Search result ${index + 1}`,
            address: item.formatted_address,
            location: cardLocation,
            zip_code: item.zip_code,
            price: Number.isInteger(parsedPrice) ? parsedPrice : 0,
            beds: Number.isInteger(parsedBeds) ? parsedBeds : 1,
            baths: Number.isInteger(parsedBaths) ? parsedBaths : 1,
            sqft: Number.isInteger(parsedSqft) ? parsedSqft : 0,
            property_type: item.property_type,
            image: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            tags: [`Score ${((item.similarity_score ?? 0) * 100).toFixed(1)}%`],
            summary: item.content || "No description provided by API.",
          };
        })
      : [];

    const sortedCards = [...cards].sort((a, b) =>
      priceSortOrder === "asc" ? a.price - b.price : b.price - a.price
    );
    const visibleCards = sortedCards.slice(0, visibleCount);
    const hasMoreResults = visibleCount < sortedCards.length;

    return (
      <div className="flex flex-col md:flex-row min-h-[calc(100vh-64px)] bg-slate-50">
        {/* Main Content */}
        <div className="flex-1 p-4 md:p-8 overflow-y-auto">
          {/* Top Search Bar & Filters */}
          <form onSubmit={handleSearch} className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 mb-8">
            <div className="flex flex-col lg:flex-row gap-4 mb-4">
              <div className="flex gap-4">
                <select
                  title="city"
                  value={cityState}
                  onChange={(event) => setCityState(event.target.value)}
                  className="bg-slate-100 border-transparent rounded-lg px-4 py-2.5 text-slate-700 focus:ring-2 focus:ring-blue-200 min-w-[140px]"
                >
                  <option>Chicago, IL</option>
                  <option>Seattle, WA</option>
                  <option>New York, NY</option>
                  <option>Austin, TX</option>
                </select>
              </div>
              <div className="relative flex-1">
                <Search className="absolute left-3 top-3 text-slate-400" size={20} />
                <input 
                  type="text" 
                  placeholder="Search by neighborhood or building name..." 
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-100 border-transparent rounded-lg focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
                />
              </div>
              <button
                type="submit"
                disabled={isSearching}
                className="px-5 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed"
              >
                {isSearching ? "Searching..." : "Search API"}
              </button>
            </div>
            {errorMessage && (
              <p className="text-sm text-red-600">{errorMessage}</p>
            )}
            {isSearching && (
              <div className="mt-4 flex items-center gap-2 text-sm text-blue-700">
                <Loader2 size={16} className="animate-spin" />
                Searching listings, please wait...
              </div>
            )}
          </form>
  
          {/* Results Header */}
          <div className="flex justify-between items-end mb-6">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Available Residences</h1>
            </div>
            <div className="flex items-center gap-2 text-sm text-slate-600">
              Sort by
              <button
                type="button"
                onClick={() => setPriceSortOrder((prev) => (prev === "asc" ? "desc" : "asc"))}
                className="font-semibold text-slate-900 flex items-center gap-1 hover:text-blue-600"
              >
                Price: {priceSortOrder === "asc" ? "Low to High" : "High to Low"} <ChevronDown size={16} />
              </button>
            </div>
          </div>
  
          {/* Property Grid */}
          {isSearching ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6 mb-10">
              {Array.from({ length: 6 }).map((_, idx) => (
                <div
                  key={`skeleton-${idx}`}
                  className={`bg-white rounded-2xl border border-slate-200 overflow-hidden ${
                    idx === 0 ? "xl:col-span-2" : ""
                  }`}
                >
                  <div className={`${idx === 0 ? "h-72" : "h-56"} bg-slate-200 animate-pulse`} />
                  <div className={`${idx === 0 ? "p-6" : "p-5"} space-y-3`}>
                    <div className="h-8 w-32 bg-slate-200 rounded animate-pulse" />
                    <div className="h-6 w-3/4 bg-slate-200 rounded animate-pulse" />
                    <div className="h-4 w-2/3 bg-slate-200 rounded animate-pulse" />
                    <div className="h-4 w-full bg-slate-200 rounded animate-pulse" />
                  </div>
                </div>
              ))}
            </div>
          ) : visibleCards.length === 0 ? (
            <div className="bg-white border border-slate-200 rounded-2xl p-10 text-center text-slate-600 mb-10">
              {hasSearched
                ? "No results found. Try another city or search keyword."
                : "Start by running a search to see available residences."}
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6 mb-10">
              {visibleCards.map((prop, index) => (
              <div
                key={prop.id}
                className={`bg-white rounded-2xl border border-slate-200 overflow-hidden hover:shadow-lg transition-all cursor-pointer group flex flex-col ${
                  index === 0 ? "xl:col-span-2" : ""
                }`}
                onClick={() => {
                  setSelectedProperty(prop);
                  setCurrentView('detail');
                }}
              >
                <div className={`relative overflow-hidden ${index === 0 ? "h-72" : "h-56"}`}>
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
                <div className={`${index === 0 ? "p-6" : "p-5"} grow flex flex-col justify-between`}>
                  <div>
                    <div className="mb-2">
                      <span className={`${index === 0 ? "text-3xl" : "text-2xl"} font-bold text-blue-600`}>${prop.price.toLocaleString()}</span>
                      <span className="text-slate-500 text-sm">/mo</span>
                    </div>
                    <h3 className={`${index === 0 ? "text-2xl" : "text-lg"} font-bold text-slate-900 group-hover:text-blue-600 transition-colors line-clamp-1`}>{prop.title}</h3>
                    <p className="text-slate-500 text-sm flex items-center gap-1 mt-1 line-clamp-1"><Map size={14} /> {prop.location}</p>
                    {prop.summary && (
                      <p className={`${index === 0 ? "text-sm" : "text-xs"} text-slate-500 mt-2 line-clamp-2`}>{prop.summary}</p>
                    )}
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
          )}
  
          <div className="flex justify-center">
            <button
              type="button"
              onClick={() => setVisibleCount((prev) => prev + RESULTS_PAGE_SIZE)}
              disabled={!hasMoreResults || visibleCards.length === 0}
              className="bg-slate-200 text-slate-700 hover:bg-slate-300 px-8 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Load More Results
            </button>
          </div>
        </div>
      </div>
    );
  };

  export default SearchView;