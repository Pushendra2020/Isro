
# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# import ee

# # Initialize Earth Engine
# ee.Initialize(project='gen-lang-client-0180648634')

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class AOIRequest(BaseModel):
#     bounds: str
#     start_date: str
#     end_date: str

# @app.post("/analyze")
# async def analyze_change(req: AOIRequest):
#     try:
#         min_lng, min_lat, max_lng, max_lat = map(float, req.bounds.split(","))
#         aoi = ee.Geometry.Rectangle([min_lng, min_lat, max_lng, max_lat])

#         # RGB for thumbnails
#         col_before_rgb = ee.ImageCollection("COPERNICUS/S2_SR") \
#             .filterBounds(aoi) \
#             .filterDate(req.start_date, req.start_date[:4] + "-12-31") \
#             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
#             .select(['B4', 'B3', 'B2']) \
#             .median()

#         col_after_rgb = ee.ImageCollection("COPERNICUS/S2_SR") \
#             .filterBounds(aoi) \
#             .filterDate(req.end_date, req.end_date[:4] + "-12-31") \
#             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
#             .select(['B4', 'B3', 'B2']) \
#             .median()

#         # For NDVI
#         col_before_ndvi = ee.ImageCollection("COPERNICUS/S2_SR") \
#             .filterBounds(aoi) \
#             .filterDate(req.start_date, req.start_date[:4] + "-12-31") \
#             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
#             .select(['B4', 'B8']) \
#             .median()

#         col_after_ndvi = ee.ImageCollection("COPERNICUS/S2_SR") \
#             .filterBounds(aoi) \
#             .filterDate(req.end_date, req.end_date[:4] + "-12-31") \
#             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
#             .select(['B4', 'B8']) \
#             .median()

#         # Check for missing bands before NDVI calculation
#         before_band_names = col_before_ndvi.bandNames().getInfo()
#         after_band_names = col_after_ndvi.bandNames().getInfo()
#         if not before_band_names or not after_band_names:
#             return {"error": "No Sentinel-2 data found for the selected AOI and date range. Try a different area or time."}
#         if not ("B4" in before_band_names and "B8" in before_band_names):
#             return {"error": "Before image does not contain required bands (B4, B8). Try a different area or time."}
#         if not ("B4" in after_band_names and "B8" in after_band_names):
#             return {"error": "After image does not contain required bands (B4, B8). Try a different area or time."}

#         ndvi_before = col_before_ndvi.normalizedDifference(['B8', 'B4']).rename('NDVI')
#         ndvi_after = col_after_ndvi.normalizedDifference(['B8', 'B4']).rename('NDVI')
#         diff = ndvi_after.subtract(ndvi_before)

#         stats = diff.reduceRegion(
#             reducer=ee.Reducer.mean(),
#             geometry=aoi,
#             scale=30,
#             maxPixels=1e9
#         )

#         mean_diff = stats.get("NDVI").getInfo()
#         confidence = min(abs(mean_diff) * 200, 100) if mean_diff else 0
#         change_detected = abs(mean_diff) > 0.05 if mean_diff else False

#         before_url = col_before_rgb.clip(aoi).visualize(
#             min=0, max=3000, bands=['B4', 'B3', 'B2']
#         ).getThumbURL({
#             'region': aoi,
#             'dimensions': 1024,
#             'format': 'png'
#         })

#         after_url = col_after_rgb.clip(aoi).visualize(
#             min=0, max=3000, bands=['B4', 'B3', 'B2']
#         ).getThumbURL({
#             'region': aoi,
#             'dimensions': 1024,
#             'format': 'png'
#         })

#         ndvi_diff_url = diff.visualize(**{
#             'min': -0.5,
#             'max': 0.5,
#             'palette': ['red', 'white', 'green']
#         }).clip(aoi).getThumbURL({
#             'region': aoi,
#             'dimensions': 1024,
#             'format': 'png'
#         })

#         # High-Res Export to Drive (Pushendra's Account)
#         export_links = {}
#         for image, name in zip([col_before_rgb, col_after_rgb, diff.visualize(**{
#             'min': -0.5, 'max': 0.5, 'palette': ['red', 'white', 'green']
#         })], ["before", "after", "ndvi"]):
#             task = ee.batch.Export.image.toDrive(**{
#                 'image': image.clip(aoi),
#                 'description': f'{name}_export',
#                 'folder': 'GEE_Exports',
#                 'fileNamePrefix': name,
#                 'scale': 10,
#                 'region': aoi
#             })
#             task.start()
#             export_links[name] = "https://drive.google.com/drive/folders"  # Placeholder, actual link shown later

#         return {
#             "change_detected": change_detected,
#             "confidence": confidence,
#             "before_img_url": before_url,
#             "after_img_url": after_url,
#             "ndvi_diff_url": ndvi_diff_url,
#             "drive_links": export_links
#         }
#     except Exception as e:
#         print("Error in /analyze:", e)
#         return {"error": str(e)}







# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# import ee

# # Initialize Earth Engine
# ee.Initialize(project='gen-lang-client-0180648634')

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class AOIRequest(BaseModel):
#     bounds: str
#     start_date: str
#     end_date: str

# @app.post("/analyze")
# async def analyze_change(req: AOIRequest):
#     try:
#         min_lng, min_lat, max_lng, max_lat = map(float, req.bounds.split(","))
#         aoi = ee.Geometry.Rectangle([min_lng, min_lat, max_lng, max_lat])

#         # RGB for thumbnails
#         col_before_rgb = ee.ImageCollection("COPERNICUS/S2_SR") \
#             .filterBounds(aoi) \
#             .filterDate(req.start_date, req.start_date[:4] + "-12-31") \
#             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
#             .select(['B4', 'B3', 'B2']) \
#             .median()

#         col_after_rgb = ee.ImageCollection("COPERNICUS/S2_SR") \
#             .filterBounds(aoi) \
#             .filterDate(req.end_date, req.end_date[:4] + "-12-31") \
#             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
#             .select(['B4', 'B3', 'B2']) \
#             .median()

#         # For NDVI
#         col_before_ndvi = ee.ImageCollection("COPERNICUS/S2_SR") \
#             .filterBounds(aoi) \
#             .filterDate(req.start_date, req.start_date[:4] + "-12-31") \
#             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
#             .select(['B4', 'B8']) \
#             .median()

#         col_after_ndvi = ee.ImageCollection("COPERNICUS/S2_SR") \
#             .filterBounds(aoi) \
#             .filterDate(req.end_date, req.end_date[:4] + "-12-31") \
#             .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
#             .select(['B4', 'B8']) \
#             .median()

#         # Check for missing bands
#         before_band_names = col_before_ndvi.bandNames().getInfo()
#         after_band_names = col_after_ndvi.bandNames().getInfo()
#         if not before_band_names or not after_band_names:
#             return {"error": "No Sentinel-2 data found for the selected AOI and date range. Try a different area or time."}
#         if not ("B4" in before_band_names and "B8" in before_band_names):
#             return {"error": "Before image does not contain required bands (B4, B8). Try a different area or time."}
#         if not ("B4" in after_band_names and "B8" in after_band_names):
#             return {"error": "After image does not contain required bands (B4, B8). Try a different area or time."}

#         ndvi_before = col_before_ndvi.normalizedDifference(['B8', 'B4']).rename('NDVI')
#         ndvi_after = col_after_ndvi.normalizedDifference(['B8', 'B4']).rename('NDVI')
#         diff = ndvi_after.subtract(ndvi_before)

#         # Pixel-count-based confidence
#         change_mask = diff.gt(0.05).Or(diff.lt(-0.05))

#         changed_pixels = change_mask.reduceRegion(
#             reducer=ee.Reducer.sum(),
#             geometry=aoi,
#             scale=30,
#             maxPixels=1e9
#         ).get('NDVI')

#         total_pixels = ee.Image(1).clip(aoi).reduceRegion(
#             reducer=ee.Reducer.count(),
#             geometry=aoi,
#             scale=30,
#             maxPixels=1e9
#         ).get('constant')

#         changed_pixels = changed_pixels.getInfo() if changed_pixels else 0
#         total_pixels = total_pixels.getInfo() if total_pixels else 1  # Prevent division by zero

#         confidence = (changed_pixels / total_pixels) * 100 if total_pixels else 0
#         change_detected = confidence > 5  # You can adjust threshold as needed

#         before_url = col_before_rgb.clip(aoi).visualize(
#             min=0, max=3000, bands=['B4', 'B3', 'B2']
#         ).getThumbURL({
#             'region': aoi,
#             'dimensions': 1024,
#             'format': 'png'
#         })

#         after_url = col_after_rgb.clip(aoi).visualize(
#             min=0, max=3000, bands=['B4', 'B3', 'B2']
#         ).getThumbURL({
#             'region': aoi,
#             'dimensions': 1024,
#             'format': 'png'
#         })

#         ndvi_diff_url = diff.visualize(**{
#             'min': -0.5,
#             'max': 0.5,
#             'palette': ['red', 'white', 'green']
#         }).clip(aoi).getThumbURL({
#             'region': aoi,
#             'dimensions': 1024,
#             'format': 'png'
#         })

#         # High-Res Export to Drive (placeholder links)
#         export_links = {}
#         for image, name in zip([col_before_rgb, col_after_rgb, diff.visualize(**{
#             'min': -0.5, 'max': 0.5, 'palette': ['red', 'white', 'green']
#         })], ["before", "after", "ndvi"]):
#             task = ee.batch.Export.image.toDrive(**{
#                 'image': image.clip(aoi),
#                 'description': f'{name}_export',
#                 'folder': 'GEE_Exports',
#                 'fileNamePrefix': name,
#                 'scale': 10,
#                 'region': aoi
#             })
#             task.start()
#             export_links[name] = "https://drive.google.com/drive/folders"  # Static placeholder

#         return {
#             "change_detected": change_detected,
#             "confidence": confidence,
#             "before_img_url": before_url,
#             "after_img_url": after_url,
#             "ndvi_diff_url": ndvi_diff_url,
#             "drive_links": export_links
#         }

#     except Exception as e:
#         print("Error in /analyze:", e)
#         return {"error": str(e)}











from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import ee

# Initialize Earth Engine
ee.Initialize(project='gen-lang-client-0180648634')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AOIRequest(BaseModel):
    bounds: str
    start_date: str
    end_date: str

@app.post("/analyze")
async def analyze_change(req: AOIRequest):
    try:
        min_lng, min_lat, max_lng, max_lat = map(float, req.bounds.split(","))
        aoi = ee.Geometry.Rectangle([min_lng, min_lat, max_lng, max_lat])

        # RGB for thumbnails
        col_before_rgb = ee.ImageCollection("COPERNICUS/S2_SR") \
            .filterBounds(aoi) \
            .filterDate(req.start_date, req.start_date[:4] + "-12-31") \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .select(['B4', 'B3', 'B2']) \
            .median()

        col_after_rgb = ee.ImageCollection("COPERNICUS/S2_SR") \
            .filterBounds(aoi) \
            .filterDate(req.end_date, req.end_date[:4] + "-12-31") \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .select(['B4', 'B3', 'B2']) \
            .median()

        # NDVI Calculation
        col_before_ndvi = ee.ImageCollection("COPERNICUS/S2_SR") \
            .filterBounds(aoi) \
            .filterDate(req.start_date, req.start_date[:4] + "-12-31") \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .select(['B4', 'B8']) \
            .median()

        col_after_ndvi = ee.ImageCollection("COPERNICUS/S2_SR") \
            .filterBounds(aoi) \
            .filterDate(req.end_date, req.end_date[:4] + "-12-31") \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .select(['B4', 'B8']) \
            .median()

        before_band_names = col_before_ndvi.bandNames().getInfo()
        after_band_names = col_after_ndvi.bandNames().getInfo()

        if not before_band_names or not after_band_names:
            return {"error": "Insufficient data for NDVI analysis. Try different dates or area."}

        ndvi_before = col_before_ndvi.normalizedDifference(['B8', 'B4']).rename('NDVI')
        ndvi_after = col_after_ndvi.normalizedDifference(['B8', 'B4']).rename('NDVI')
        diff = ndvi_after.subtract(ndvi_before)

        stats = diff.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=aoi,
            scale=30,
            maxPixels=1e9
        )

        mean_diff = stats.get("NDVI").getInfo()
        confidence = min(abs(mean_diff) * 200, 100) if mean_diff else 0
        change_detected = abs(mean_diff) > 0.05 if mean_diff else False

        # Before & After Image URLs
        before_url = col_before_rgb.clip(aoi).visualize(min=0, max=3000, bands=['B4', 'B3', 'B2']).getThumbURL({
            'region': aoi,
            'dimensions': 1024,
            'format': 'png'
        })

        # After image with major change outline
        ndvi_threshold = 0.1
        raw_change = diff.gt(ndvi_threshold).Or(diff.lt(-ndvi_threshold))
        large_change = raw_change.connectedPixelCount(200, True).gt(100)
        smoothed_change = large_change.focal_max(1)
        after_visual = col_after_rgb.clip(aoi).visualize(min=0, max=3000, bands=['B4', 'B3', 'B2'])

        change_outline = smoothed_change.reduceToVectors(scale=10, geometryType='polygon', geometry=aoi)
        change_layer = ee.Image().paint(change_outline, color=1, width=2).visualize(palette=['blue'])

        after_with_changes = after_visual.blend(change_layer)

        after_url = after_with_changes.getThumbURL({
            'region': aoi,
            'dimensions': 1024,
            'format': 'png'
        })

        # NDVI Change Map
        ndvi_diff_url = diff.visualize(min=-0.5, max=0.5, palette=['red', 'white', 'green']).clip(aoi).getThumbURL({
            'region': aoi,
            'dimensions': 1024,
            'format': 'png'
        })

        return {
            "change_detected": change_detected,
            "confidence": confidence,
            "before_img_url": before_url,
            "after_img_url": after_url,
            "ndvi_diff_url": ndvi_diff_url
        }

    except Exception as e:
        print("Error in /analyze:", e)
        return {"error": str(e)}
