# MODIS Fire Data — Metadata & Provenance

## Data Source & License

### Source

- **Product Name**: MODIS Fire and Thermal Anomalies Collection 6.1 (MCD14ML)
- **Provider**: NASA (National Aeronautics & Space Administration)
- **Download Portal**: [NASA FIRMS (Fire Information for Resource Management System)](https://firms.modaps.eosdis.nasa.gov/)
- **License**: Public Domain (no restrictions, but please cite NASA)
- **Spatial Coverage**: India (region: ~5°N to 35°N, 65°E to 97°E)
- **Temporal Range**: 2021-01-01 to 2023-12-31

### Citation & Acknowledgments

**Required Attribution:**

```
Data source: NASA FIRMS
Giglio et al. (2016). The Collection 6 MODIS active fire detection algorithm and fire products. 
Remote Sensing of Environment, 178, 31-41.
```

When publishing results using this data, cite:

- **Giglio, L.**, W. Schroeder, & C.O. Justice (2016), The Collection 6 MODIS active fire detection algorithm and fire products, *Remote Sensing of Environment*, 178, 31-41.
- **NASA**: Access FIRMS data at https://firms.modaps.eosdis.nasa.gov/

---

## Column Descriptions

### Geospatial

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| `latitude` | float | -90 to 90 | Fire detection latitude (WGS84 datum) |
| `longitude` | float | -180 to 180 | Fire detection longitude (WGS84 datum) |

**Spatial Accuracy**: ±0.5 km for Terra; ±1–2 km for Aqua (due to orbit geometry)

### Thermal Data

| Column | Type | Units | Range | Description |
|--------|------|-------|-------|-------------|
| `brightness` | float | Kelvin (K) | 280–400 | Mid-infrared brightness temperature (Band 21, 3.9 μm) |
| `brightness_t31` | float | Kelvin (K) | 250–330 | Thermal IR brightness (Band 31, 11 μm); surface temperature proxy |
| `frp` | float | Megawatts (MW) | 0–500+ | Fire Radiative Power; total heat released by fire |

**Notes:**
- Higher `brightness` indicates stronger thermal signal (hotter fire)
- `frp` correlates with burn area and fire intensity
- `brightness_t31` helps distinguish cloud from fire (fires warm in both IR and thermal)

### Metadata

| Column | Type | Values | Description |
|--------|------|--------|-------------|
| `confidence` | int | 0–100 | Algorithm confidence in fire detection (%) |
| `type` | int | 0, 1, 2, 3 | Fire type classification (see below) |
| `acq_date` | string | YYYY-MM-DD | Acquisition date (UTC) |
| `acq_time` | string | HHMM (24h) | Acquisition time (UTC) |
| `satellite` | string | "T" or "A" | Terra (T) or Aqua (A) |

### Fire Type Classification (Target Variable)

| Type | Code | Description | Typical Characteristics |
|------|------|-------------|------------------------|
| **Vegetation** | 0 | Forest, crop, grassland fires | High `brightness`, high `frp`, spatial clustering |
| **Static** | 1 | Volcanoes, geothermal, urban heating | Persistent location, moderate `brightness` |
| **Offshore** | 2 | Ocean/water surface thermal anomalies | Over water; low `frp` |
| **Volcano** | 3 | Active volcanic activity | High stability, distinct thermal signature |

---

## Data Preprocessing & Quality Considerations

### Filtering Applied

```python
# Recommended preprocessing:
df = df[df['confidence'] >= 50]           # Remove low-confidence detections
df = df[df['acq_date'] >= '2021-01-01']   # Date range filtering
df = df[df['acq_date'] <= '2023-12-31']
df = df.drop_duplicates()                  # Remove exact duplicates
```

### Known Issues & Artifacts

1. **False Positives** (2–5% of detections):
   - Clouds with high thermal contrast
   - Flares from oil/gas facilities
   - Urban areas with high surface temperatures
   - **Mitigation**: Use `confidence >= 75` for critical applications

2. **Geolocation Errors**:
   - Terra: Generally ±0.5 km
   - Aqua: ±1–2 km (historical orbit drift)
   - **Mitigation**: Use confidence weighting; spatial aggregation

3. **Temporal Lag**:
   - Near Real-Time (NRT) data: ~3 hours
   - Standard data: ~1 day
   - **Note**: Use NRT for alerts; Standard for analysis

4. **Saturation**:
   - Very large fires may saturate brightness sensors
   - `frp` typically maxes out ~100–200 MW for saturation
   - **Mitigation**: Use threshold at 80–90 for confidence intervals

### Class Imbalance

From 2023 India data:

| Type | Count | Percentage |
|------|-------|-----------|
| Vegetation (0) | ~12,500 | 71% |
| Static (1) | ~3,200 | 18% |
| Offshore (2) | ~1,600 | 9% |
| Volcano (3) | ~100 | 0.6% |

**Solutions in modeling**:
- Use `stratified_train_test_split()` (scikit-learn)
- Report F1 scores per class, not just accuracy
- Consider weighted loss functions for imbalanced classes

---

## Column Descriptions (Extended)

### Optional/Derived Columns (added during preprocessing)

| Column | Type | Description |
|--------|------|-------------|
| `month` | int | Month of detection (1–12) |
| `day_of_year` | int | Day of year (1–366) |
| `hour` | int | Hour of day (0–23, from `acq_time`) |
| `brightness_diff` | float | `brightness - brightness_t31` (fire signature) |
| `frp_per_pixel` | float | FRP normalized (research use) |
| `confidence_category` | string | "low", "medium", "high" (binned from `confidence`) |

---

## Files & Sizes

### Raw Data (not tracked, .gitignore)

```
data/raw/
├── modis_2021_India.csv     ~8.65 MB (~22,000 rows)
├── modis_2022_India.csv     ~6.34 MB (~17,000 rows)
└── modis_2023_India.csv     ~6.17 MB (~17,500 rows)
                            ─────────────────────
                       Total: ~21 MB, ~56,500 rows
```

### Sample Data (tracked, for CI/testing)

```
data/sample/
└── modis_2023_sample.csv   ~1 MB (~2,500 rows, random sample of 2023)
```

---

## Data Download Instructions

### From NASA FIRMS (Recommended)

1. Visit: https://firms.modaps.eosdis.nasa.gov/download/
2. Select:
   - **Region**: India
   - **Dates**: 2021-01-01 to 2023-12-31
   - **Satellite**: All (combines Terra + Aqua)
   - **Format**: CSV
3. Download and place in `data/raw/`

### Alternative: Using Google Earth Engine

```python
import ee

ee.Initialize()
dataset = ee.ImageCollection('MODIS/006/MOD14A1') \
  .filterDate('2021-01-01', '2023-12-31') \
  .filterBounds(geometry)  # India bounds
```

---

## Validation & Quality Assurance

### Consistency Checks

```python
# Run these to validate data integrity
assert df['latitude'].between(-90, 90).all(), "Invalid latitude"
assert df['longitude'].between(-180, 180).all(), "Invalid longitude"
assert df['confidence'].between(0, 100).all(), "Invalid confidence"
assert df['type'].isin([0, 1, 2, 3]).all(), "Invalid fire type"
assert df['brightness'].min() > 200, "Brightness too low (check units)"
```

### Data Completeness

For each year:
- Check for gaps in temporal coverage
- Verify satellite overlap (Terra + Aqua consistency)
- Flag any anomalies or sensor outages (NASA MODIS Status)

---

## References & Further Reading

### MODIS Fire Product Documentation

- **[MODIS Active Fire Product Guide](https://lpdaac.usgs.gov/products/mod14a1v061/)**: Full technical documentation
- **[MODIS Bands Reference](https://modis.gsfc.nasa.gov/about/specifications.php)**: Spectral band details
- **[FIRMS User Guide](https://www.earthdata.nasa.gov/data/tools/firms)**: Download & interpretation

### Academic References

1. Giglio, L., Schroeder, W., & Justice, C. O. (2016). The Collection 6 MODIS active fire detection algorithm and fire products. *Remote Sensing of Environment*, 178, 31–41.
2. Schroeder, W., Oliva, P., Giglio, L., & Csiszar, I. A. (2014). The New VIIRS 375m active fire detection data product: Algorithm description and validation. *Journal of Geophysical Research*, 119(5), 2751–2771.
3. Justice, C. O., Giglio, L., Korontzi, S., et al. (2002). The MODIS fire products. *Remote Sensing Reviews*, 88(3–4), 242–253.

### Ethical & Policy Context

- **[UN Office for Disaster Risk Reduction (UNDRR)](https://www.undrr.org/)**: Global disaster risk framework
- **[Global Disaster Alert & Coordination System (GDACS)](https://www.gdacs.org/)**: Real-time disaster monitoring
- **[India's National Action Plan on Climate Change (NAPCC)](http://moef.gov.in/)**: Fire management policy

---

## Data Sharing & Redistribution

### Allowed

✅ Use for research & analysis  
✅ Share findings & publications  
✅ Combine with other open data  
✅ Create derivative works  

### Required

📋 Cite NASA/FIRMS  
📋 Acknowledge data source in publications  
📋 Retain attribution in redistributed data  

### Restricted

❌ Claim data as your own  
❌ Sell data without modification  
❌ Remove attribution  

---

## Contact & Support

- **Questions about data**: [FIRMS Support](https://www.earthdata.nasa.gov/data/tools/firms)
- **Technical issues**: [NASA LP DAAC](https://lpdaac.usgs.gov/)
- **Project questions**: [GitHub Issues](https://github.com/1511Darshan/AICTE-FIRE-CLASSIFICATION/issues)

---

**Last Updated**: November 2025  
**Data Version**: MODIS Collection 6.1  
**Status**: ✅ Active & Maintained
