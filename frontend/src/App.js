
import { useState, useEffect } from 'react';
import "./App.css";
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [companyInfo, setCompanyInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Sample data for mockup - will be replaced with actual API calls
  const mockCompanyData = {
    name: "Acme Corporation",
    industry: "Technology",
    quirkNews: [
      {
        headline: "Acme CEO Starts Office Alpaca Farm to 'Boost Morale'",
        source: "Tech Daily",
        date: "March 15, 2025",
        quirkFactor: 4,
        summary: "In an unusual workplace initiative, Acme's CEO has introduced a herd of alpacas to company headquarters, claiming they improve creativity and reduce stress.",
        sentiment: "😂",
        url: "#"
      },
      {
        headline: "Acme's AI Assistant Accidentally Orders 10,000 Rubber Ducks",
        source: "Business Insider",
        date: "March 10, 2025",
        quirkFactor: 5,
        summary: "A glitch in Acme's new AI procurement system resulted in thousands of rubber ducks being delivered to their main office. Employees have turned it into an impromptu charity drive.",
        sentiment: "😮",
        url: "#"
      },
      {
        headline: "Acme Introduces 'Bring Your Pet Rock to Work' Day",
        source: "Corporate Culture Today",
        date: "March 5, 2025",
        quirkFactor: 3,
        summary: "In a throwback to the 1970s, Acme has instituted a monthly event where employees bring decorated pet rocks to work, complete with a contest for 'Most Innovative Rock'.",
        sentiment: "🤔",
        url: "#"
      }
    ]
  };

  useEffect(() => {
    const fetchCompanyInfo = async () => {
      try {
        // Using the environment variable for backend URL
        const response = await fetch(`${BACKEND_URL}/api/company-info?name=Acme Corporation`);
        if (!response.ok) throw new Error('Failed to fetch company info');
        const data = await response.json();
        setCompanyInfo(data);
      } catch (err) {
        console.error("Error fetching company info:", err);
        // Fallback to mock data if API fails
        setCompanyInfo(mockCompanyData);
        setError("Using sample data (API connection issue)");
      } finally {
        setLoading(false);
      }
    };
    
    fetchCompanyInfo();
  }, []);

  // Helper function to render quirk factor stars
  const renderQuirkFactor = (factor) => {
    return Array(5).fill(0).map((_, index) => (
      <span key={index} className={`text-xl ${index < factor ? 'text-yellow-400' : 'text-gray-300'}`}>★</span>
    ));
  };

  if (loading) return (
    <div className="flex justify-center items-center h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
    </div>
  );

  if (error) return (
    <div className="text-red-500 text-center p-4">
      Error: {error}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* HubSpot Card Container */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
          {/* Card Header */}
          <div className="bg-gradient-to-r from-purple-600 to-indigo-600 px-6 py-4 flex justify-between items-center">
            <div className="flex items-center">
              <span className="text-white text-2xl font-bold">Quirky News Radar</span>
              <span className="ml-2 text-3xl">🔍</span>
            </div>
            <div className="text-white opacity-80">
              Last updated: {new Date().toLocaleDateString()}
            </div>
          </div>
          
          {/* Company Info Section */}
          <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
            <h2 className="text-2xl font-bold text-gray-800">{companyInfo.name}</h2>
            <p className="text-gray-600">{companyInfo.industry}</p>
          </div>
          
          {/* News Items */}
          <div className="p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Unusual & Amusing Company News</h3>
            
            {companyInfo.quirkNews.map((item, index) => (
              <div key={index} className="mb-6 bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow p-4">
                <div className="flex justify-between">
                  <h4 className="text-xl font-semibold text-gray-800 mb-2">{item.headline}</h4>
                  <span className="text-2xl">{item.sentiment}</span>
                </div>
                
                <div className="flex items-center text-sm text-gray-500 mb-2">
                  <span>{item.source}</span>
                  <span className="mx-2">•</span>
                  <span>{item.date}</span>
                </div>
                
                <div className="flex items-center mb-3">
                  <span className="text-sm font-medium text-gray-700 mr-2">Quirk Factor:</span>
                  <div className="flex">
                    {renderQuirkFactor(item.quirkFactor)}
                  </div>
                </div>
                
                <p className="text-gray-700 mb-3">{item.summary}</p>
                
                <a href={item.url} 
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                  Read Full Story
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              </div>
            ))}
            
            {/* Empty State */}
            {companyInfo.quirkNews.length === 0 && (
              <div className="text-center py-8">
                <div className="text-4xl mb-4">🔍</div>
                <h4 className="text-xl font-medium text-gray-700">No quirky news found</h4>
                <p className="text-gray-500">We're keeping an eye out for interesting stories about this company.</p>
              </div>
            )}
          </div>
          
          {/* Card Footer */}
          <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 text-right">
            <button className="text-sm text-indigo-600 hover:text-indigo-800 focus:outline-none">
              Refresh News
            </button>
          </div>
        </div>
        
        {/* HubSpot Settings Preview (for demo) */}
        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">HubSpot Integration Settings</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="col-span-2 sm:col-span-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">News Refresh Frequency</label>
              <select className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
                <option>Daily</option>
                <option>Weekly</option>
                <option>Monthly</option>
              </select>
            </div>
            <div className="col-span-2 sm:col-span-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">Quirk Factor Minimum</label>
              <select className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
                <option>1 - Show All News</option>
                <option>2 - Slightly Unusual</option>
                <option>3 - Definitely Quirky</option>
                <option>4 - Very Unusual</option>
                <option>5 - Completely Off The Wall</option>
              </select>
            </div>
            <div className="col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">News Categories</label>
              <div className="mt-2 grid grid-cols-2 gap-2">
                <div className="flex items-center">
                  <input type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label className="ml-2 block text-sm text-gray-700">Funny</label>
                </div>
                <div className="flex items-center">
                  <input type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label className="ml-2 block text-sm text-gray-700">Unusual</label>
                </div>
                <div className="flex items-center">
                  <input type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label className="ml-2 block text-sm text-gray-700">Surprising</label>
                </div>
                <div className="flex items-center">
                  <input type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" />
                  <label className="ml-2 block text-sm text-gray-700">Controversial</label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
