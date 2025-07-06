# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# import ee
# import numpy as np
# print(ee.__version__)

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
#     bounds: str  # bbox as "minLng,minLat,maxLng,maxLat"
#     start_date: str
#     end_date: str

# @app.post("/analyze")
# async def analyze_change(req: AOIRequest):
#     min_lng, min_lat, max_lng, max_lat = map(float, req.bounds.split(","))
#     aoi = ee.Geometry.Rectangle([min_lng, min_lat, max_lng, max_lat])

#     col_before = ee.ImageCollection("COPERNICUS/S2_SR") \
#         .filterBounds(aoi) \
#         .filterDate(req.start_date, req.start_date[:4] + "-12-31") \
#         .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
#         .median()

#     col_after = ee.ImageCollection("COPERNICUS/S2_SR") \
#         .filterBounds(aoi) \
#         .filterDate(req.end_date, req.end_date[:4] + "-12-31") \
#         .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
#         .median()

#     ndvi_before = col_before.normalizedDifference(['B8', 'B4']).rename('NDVI')
#     ndvi_after = col_after.normalizedDifference(['B8', 'B4']).rename('NDVI')

#     before_url = col_before.getThumbURL({
#         'region': aoi,
#         'dimensions': 256,
#         'format': 'png'
#     })

#     after_url = col_after.getThumbURL({
#         'region': aoi,
#         'dimensions': 256,
#         'format': 'png'
#     })

#     ndvi_diff_url = diff.visualize(**{
#         'min': -0.5,
#         'max': 0.5,
#         'palette': ['red', 'white', 'green']
#     }).getThumbURL({
#         'region': aoi,
#         'dimensions': 256,
#         'format': 'png'
#     })



#     diff = ndvi_after.subtract(ndvi_before)
#     stats = diff.reduceRegion(
#         reducer=ee.Reducer.mean(),
#         geometry=aoi,
#         scale=30,
#         maxPixels=1e9
#     )

#     mean_diff = stats.get("NDVI").getInfo()

#     # Confidence based on magnitude of NDVI change
#     confidence = min(abs(mean_diff) * 200, 100) if mean_diff else 0
#     change_detected = abs(mean_diff) > 0.05 if mean_diff else False

#     return {
#     "change_detected": change_detected,
#     "confidence": confidence,
#     "before_img_url": before_url,
#     "after_img_url": after_url,
#     "ndvi_diff_url": ndvi_diff_url
#     }










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

        col_before = ee.ImageCollection("COPERNICUS/S2_SR") \
        .filterBounds(aoi) \
        .filterDate(req.start_date, req.start_date[:4] + "-12-31") \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .median()

        col_after = ee.ImageCollection("COPERNICUS/S2_SR") \
        .filterBounds(aoi) \
        .filterDate(req.end_date, req.end_date[:4] + "-12-31") \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .median()

        ndvi_before = col_before.normalizedDifference(['B8', 'B4']).rename('NDVI')
        ndvi_after = col_after.normalizedDifference(['B8', 'B4']).rename('NDVI')
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

        before_url = col_before.clip(aoi).getThumbURL({
        'region': aoi,
        'dimensions': 256,
        'format': 'png'
        })

        after_url = col_after.clip(aoi).getThumbURL({
        'region': aoi,
        'dimensions': 256,
        'format': 'png'
        })

        ndvi_diff_url = diff.visualize(**{
        'min': -0.5,
        'max': 0.5,
        'palette': ['red', 'white', 'green']
        }).clip(aoi).getThumbURL({
        'region': aoi,
        'dimensions': 256,
        'format': 'png'
        })

    # High-Res Export to Drive (Pushendra's Account)
        export_links = {}
        for image, name in zip([col_before, col_after, diff.visualize(**{
            'min': -0.5, 'max': 0.5, 'palette': ['red', 'white', 'green']
        })], ["before", "after", "ndvi"]):
            task = ee.batch.Export.image.toDrive(**{
            'image': image.clip(aoi),
            'description': f'{name}_export',
            'folder': 'GEE_Exports',
            'fileNamePrefix': name,
            'scale': 10,
            'region': aoi
            })
            task.start()
            export_links[name] = "https://drive.google.com/drive/folders"  # Placeholder, actual link shown later

        return {
            "change_detected": change_detected,
            "confidence": confidence,
            "before_img_url": before_url,
            "after_img_url": after_url,
            "ndvi_diff_url": ndvi_diff_url,
            "drive_links": export_links
            }
    except Exception as e:
        print("Error in /analyze:", e)
        return {"error": str(e)}