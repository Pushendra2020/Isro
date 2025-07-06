// import { useState } from "react";
// import { MapContainer, TileLayer, Rectangle, Marker, useMapEvents } from "react-leaflet";
// import "leaflet/dist/leaflet.css";
// import L from "leaflet";
// import DatePicker from "react-datepicker";
// import "react-datepicker/dist/react-datepicker.css";
// import { CalendarIcon } from "lucide-react";

// export default function AOIChangeDetection() {
//   const [corner1, setCorner1] = useState(null);
//   const [corner2, setCorner2] = useState(null);
//   const [startDate, setStartDate] = useState(new Date());
//   const [endDate, setEndDate] = useState(new Date());
//   const [result, setResult] = useState(null);

//   const BoundsSelector = () => {
//     useMapEvents({
//       click(e) {
//         if (!corner1) {
//           setCorner1(e.latlng);
//         } else if (!corner2) {
//           setCorner2(e.latlng);
//         } else {
//           setCorner1(e.latlng);
//           setCorner2(null);
//         }
//       },
//     });
//     return null;
//   };

//   const analyzeChange = async () => {
//     if (!corner1 || !corner2) return alert("Please select two corners on the map.");
//     const bounds = L.latLngBounds(corner1, corner2);
//     const body = {
//       bounds: bounds.toBBoxString(),
//       start_date: startDate.toISOString().split("T")[0],
//       end_date: endDate.toISOString().split("T")[0],
//     };

//     const res = await fetch("http://localhost:8000/analyze", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(body),
//     });

//     const data = await res.json();
//     setResult(data);
//   };

//   return (
//     <div className="p-4 space-y-4">
//       <h2 className="text-xl font-bold mb-2">Select Area & Dates</h2>

//       <div className="flex space-x-4 mb-4">
//         <div>
//           <label className="block">Start Date</label>
//           <DatePicker selected={startDate} onChange={(date) => setStartDate(date)} dateFormat="yyyy-MM-dd" />
//         </div>
//         <div>
//           <label className="block">End Date</label>
//           <DatePicker selected={endDate} onChange={(date) => setEndDate(date)} dateFormat="yyyy-MM-dd" />
//         </div>
//       </div>

//       <MapContainer center={[20.5937, 78.9629]} zoom={5} style={{ height: "400px" }}>
//         <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
//         <BoundsSelector />
//         {corner1 && <Marker position={corner1} />}
//         {corner2 && <Marker position={corner2} />}
//         {corner1 && corner2 && <Rectangle bounds={[corner1, corner2]} pathOptions={{ color: "red" }} />}
//       </MapContainer>

//       <button className="mt-4 p-2 bg-blue-500 text-white rounded" onClick={analyzeChange}>
//         Analyze Change
//       </button>

//       {result && (
//   <div className="mt-4 space-y-4">
//     <h3 className="text-lg font-bold">Analysis Result:</h3>
//     <p>Man-made Change: {result.change_detected ? "YES" : "NO"}</p>
//     <p>Confidence Score: {result.confidence.toFixed(2)}%</p>

//     <h4 className="text-md font-bold mt-4">Proof of Analysis:</h4>
//     <div className="grid grid-cols-3 gap-4">
//       <div>
//         <p className="font-semibold">Before Image</p>
//         <img src={result.before_img_url} alt="Before" className="border" />
//       </div>
//       <div>
//         <p className="font-semibold">After Image</p>
//         <img src={result.after_img_url} alt="After" className="border" />
//       </div>
//       <div>
//         <p className="font-semibold">NDVI Change Map</p>
//         <img src={result.ndvi_diff_url} alt="NDVI Difference" className="border" />
//       </div>
//     </div>
//   </div>
// )}
//     </div>
//   );
// }



import { useState } from "react";
import { MapContainer, TileLayer, Rectangle, Marker, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { CalendarIcon } from "lucide-react";
import axios from "axios";

export default function AOIChangeDetection() {
  const [corner1, setCorner1] = useState(null);
  const [corner2, setCorner2] = useState(null);
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [result, setResult] = useState(null);

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

    try {
      const res = await axios.post("http://localhost:8000/analyze", body, {
        headers: { "Content-Type": "application/json" },
      });
      setResult(res.data);
    } catch (err) {
      alert("Error: " + (err.response?.data?.error || err.message));
    }
  };

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-xl font-bold mb-2">Select Area & Dates</h2>

      <div className="flex space-x-4 mb-4">
        <div>
          <label className="block">Start Date</label>
          <DatePicker selected={startDate} onChange={(date) => setStartDate(date)} dateFormat="yyyy-MM-dd" />
        </div>
        <div>
          <label className="block">End Date</label>
          <DatePicker selected={endDate} onChange={(date) => setEndDate(date)} dateFormat="yyyy-MM-dd" />
        </div>
      </div>

      <MapContainer center={[20.5937, 78.9629]} zoom={5} style={{ height: "400px" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <BoundsSelector />
        {corner1 && <Marker position={corner1} />} 
        {corner2 && <Marker position={corner2} />} 
        {corner1 && corner2 && <Rectangle bounds={[corner1, corner2]} pathOptions={{ color: "red" }} />} 
      </MapContainer>

      <button className="mt-4 p-2 bg-blue-500 text-white rounded" onClick={analyzeChange}>
        Analyze Change
      </button>

      {result && (
        <div className="mt-4 space-y-4">
          <h3 className="text-lg font-bold">Analysis Result:</h3>
          <p>Man-made Change: {result.change_detected ? "YES" : "NO"}</p>
          {/* <p>Confidence Score: {result.confidence.toFixed(2)}%</p> */}

          <h4 className="text-md font-bold mt-4">Proof of Analysis:</h4>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <p className="font-semibold">Before Image</p>
              <img src={result.before_img_url} alt="Before" className="border" />
            </div>
            <div>
              <p className="font-semibold">After Image</p>
              <img src={result.after_img_url} alt="After" className="border" />
            </div>
            <div>
              <p className="font-semibold">NDVI Change Map</p>
              <img src={result.ndvi_diff_url} alt="NDVI Difference" className="border" />
            </div>
          </div>

          {result.drive_links && (
            <div className="mt-4">
              <p className="font-semibold">Full-Resolution Downloads:</p>
              <ul className="list-disc list-inside">
                <li><a href={result.drive_links.before} target="_blank" className="text-blue-600 underline">Before Image</a></li>
                <li><a href={result.drive_links.after} target="_blank" className="text-blue-600 underline">After Image</a></li>
                <li><a href={result.drive_links.ndvi} target="_blank" className="text-blue-600 underline">NDVI Change Map</a></li>
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
