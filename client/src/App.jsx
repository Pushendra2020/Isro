import { useState } from "react";
import { MapContainer, TileLayer, Rectangle, Marker, useMapEvents, Tooltip } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { CalendarIcon } from "lucide-react";
import axios from "axios";
import beforeImg from './assets/befor.png';
import afterImg from './assets/after.png';

export default function AOIChangeDetection() {
  const [corner1, setCorner1] = useState(null);
  const [corner2, setCorner2] = useState(null);
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const BoundsSelector = () => {
    useMapEvents({
      click(e) {
        if (!corner1) {
          setCorner1(e.latlng);
        } else if (!corner2) {
          setCorner2(e.latlng);
        } else {
          setCorner1(e.latlng);
          setCorner2(null);
        }
      },
    });
    return null;
  };

  const analyzeChange = async () => {
    if (!corner1 || !corner2) return alert("Please select two corners on the map.");
    const bounds = L.latLngBounds(corner1, corner2);
    const body = {
      bounds: bounds.toBBoxString(),
      start_date: startDate.toISOString().split("T")[0],
      end_date: endDate.toISOString().split("T")[0],
    };

    setLoading(true);
    setResult(null);
    try {
      const res = await axios.post("http://localhost:8000/analyze", body, {
        headers: { "Content-Type": "application/json" },
      });
      setResult(res.data);
    } catch (err) {
      alert("Error: " + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-100 flex flex-col items-center py-2">
      <style>{`
        .fade-in {
          animation: fadeIn 0.7s cubic-bezier(.4,0,.2,1);
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: scale(0.97); }
          to { opacity: 1; transform: scale(1); }
        }
        .spin {
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        /* Fix react-datepicker z-index */
        .react-datepicker-popper {
          z-index: 9999 !important;
        }
      `}</style>
      <div className="w-full max-w-[1800px] bg-white rounded-2xl shadow-xl p-2 md:p-4 space-y-4 border border-gray-200 satellite-glow">
        <h2 className="text-3xl font-extrabold text-center text-blue-700 mb-4 tracking-tight drop-shadow ml-gradient rounded-xl py-2 satellite-border">AOI Change Detection</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 md:gap-4 items-stretch min-h-[80vh]">
          {/* Map Section */}
          <div className="flex flex-col gap-2 h-full justify-stretch">
            <div className="rounded-xl overflow-hidden shadow-lg border border-gray-300 flex-1 min-h-[400px]">
              <MapContainer center={[20.5937, 78.9629]} zoom={5} style={{ height: "100%", width: "100%" }}>
                <TileLayer
                  url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                  attribution="&copy; <a href='https://www.esri.com/en-us/home'>Esri</a> &mdash; Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community"
                />
                <BoundsSelector />
                {corner1 && <Marker position={corner1}>
                  <Tooltip direction="top" offset={[0, -20]} opacity={1} permanent className="bg-white text-blue-700 font-bold rounded shadow px-2 py-1 satellite-glow">
                    Corner 1
                  </Tooltip>
                </Marker>}
                {corner2 && <Marker position={corner2}>
                  <Tooltip direction="top" offset={[0, -20]} opacity={1} permanent className="bg-white text-green-700 font-bold rounded shadow px-2 py-1 satellite-glow">
                    Corner 2
                  </Tooltip>
                </Marker>}
                {corner1 && corner2 && <Rectangle bounds={[corner1, corner2]} pathOptions={{ color: "#e11d48", weight: 3, dashArray: '8 4' }}>
                  <Tooltip direction="center" opacity={1} permanent className="bg-white text-pink-700 font-bold rounded shadow px-2 py-1 satellite-glow">
                    AOI (Selected Area)
                  </Tooltip>
                </Rectangle>}
              </MapContainer>
            </div>
            <div className="flex flex-col md:flex-row gap-2 w-full">
              <div className="flex flex-col items-center w-full">
                <label className="block text-lg font-semibold mb-2 text-gray-700">Start Date</label>
                <DatePicker
                  selected={startDate}
                  onChange={(date) => setStartDate(date)}
                  dateFormat="yyyy-MM-dd"
                  className="border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 w-full"
                  popperPlacement="bottom"
                  popperClassName="z-50"
                  portalId="root-portal"
                />
              </div>
              <div className="flex flex-col items-center w-full">
                <label className="block text-lg font-semibold mb-2 text-gray-700">End Date</label>
                <DatePicker
                  selected={endDate}
                  onChange={(date) => setEndDate(date)}
                  dateFormat="yyyy-MM-dd"
                  className="border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 w-full"
                  popperPlacement="bottom"
                  popperClassName="z-50"
                  portalId="root-portal"
                />
              </div>
            </div>
            <button className="w-full md:w-auto mt-2 px-8 py-3 bg-gradient-to-r from-blue-600 to-green-500 text-white text-lg font-bold rounded-lg shadow hover:from-blue-700 hover:to-green-600 transition-all duration-200 active:scale-95 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2" onClick={analyzeChange} disabled={loading}>
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="w-6 h-6 mr-2 spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                  </svg>
                  Analyzing...
                </span>
              ) : (
                'Analyze Change'
              )}
            </button>
            {loading && (
              <div className="flex flex-col items-center mt-8 fade-in">
                <svg className="w-16 h-16 text-blue-500 spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
                </svg>
                <p className="mt-4 text-blue-700 font-semibold animate-pulse">Processing satellite data...</p>
              </div>
            )}
          </div>
          {/* Result Section */}
          <div className="flex flex-col h-full justify-stretch">
            {result && !loading && (
              <div className="fade-in flex flex-col gap-4 h-full justify-stretch">
                <h3 className="text-2xl font-bold text-green-700 text-left md:text-center">Analysis Result</h3>
                <div className="flex flex-col md:flex-row gap-2">
                  <div className="flex-1 bg-blue-50 rounded-lg p-2 shadow text-center transition-all duration-300 hover:scale-105 fade-in">
                    <p className="text-base font-semibold">Man-made Change:</p>
                    <p className={`text-lg font-bold ${result.change_detected ? 'text-red-600' : 'text-green-600'}`}>{result.change_detected ? "YES" : "NO"}</p>
                  </div>
                  <div className="flex-1 bg-green-50 rounded-lg p-2 shadow text-center transition-all duration-300 hover:scale-105 fade-in">
                    <p className="text-base font-semibold">Confidence Score:</p>
                    <p className="text-lg font-bold text-blue-700">{result.confidence?.toFixed(2)}%</p>
                  </div>
                </div>
                <h4 className="text-xl font-bold mt-4 text-gray-700">Proof of Analysis</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1">
                  <div className="bg-white rounded-lg shadow p-0 flex flex-col items-center transition-all duration-300 hover:scale-105 fade-in h-full">
                    <p className="font-semibold mb-1 text-xs text-gray-600">Before Image</p>
                    <div className="w-full flex items-center justify-center min-h-[180px] max-h-[320px] md:max-h-[340px]">
                      <img
                        src={result?.drive_links?.before || beforeImg}
                        alt="Before"
                        className="border rounded-lg object-contain w-full h-auto max-h-[320px] md:max-h-[340px] aspect-video bg-gray-100 transition-all duration-500 hover:shadow-xl hover:scale-105"
                        style={{ maxHeight: '100%', maxWidth: '100%' }}
                      />
                    </div>
                  </div>
                  <div className="bg-white rounded-lg shadow p-0 flex flex-col items-center transition-all duration-300 hover:scale-105 fade-in h-full">
                    <p className="font-semibold mb-1 text-xs text-gray-600">After Image</p>
                    <div className="w-full flex items-center justify-center min-h-[180px] max-h-[320px] md:max-h-[340px]">
                      <img
                        src={result?.drive_links?.after || afterImg}
                        alt="After"
                        className="border rounded-lg object-contain w-full h-auto max-h-[320px] md:max-h-[340px] aspect-video bg-gray-100 transition-all duration-500 hover:shadow-xl hover:scale-105"
                        style={{ maxHeight: '100%', maxWidth: '100%' }}
                      />
                    </div>
                  </div>
                  <div className="bg-white rounded-lg shadow p-0 flex flex-col items-center transition-all duration-300 hover:scale-105 fade-in h-full">
                    <p className="font-semibold mb-1 text-xs text-gray-600">NVDI Image</p>
                    <div className="w-full flex items-center justify-center min-h-[180px] max-h-[320px] md:max-h-[340px]">
                      <img
                        src={result?.ndvi_diff_url}
                        alt="NDVI"
                        className="border rounded-lg object-contain w-full h-auto max-h-[320px] md:max-h-[340px] aspect-video bg-gray-100 transition-all duration-500 hover:shadow-xl hover:scale-105"
                        style={{ maxHeight: '100%', maxWidth: '100%' }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div >
  );
}
