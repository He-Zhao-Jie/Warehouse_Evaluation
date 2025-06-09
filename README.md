# Warehouse Evaluation System

A sophisticated real estate analysis system built with Streamlit, focusing on warehouse property valuation using spatial interpolation techniques and statistical analysis.

## 🌟 Features

### Interactive Mapping
- Dynamic Folium-based mapping interface with fullscreen capability
- Color-coded markers for target and comparison properties
- Detailed property information in popup windows
- Real-time distance calculations

### Advanced Filtering
- Distance-based filtering with adjustable radius (0-50km)
- Area-based filtering with customizable tolerance ranges
- Dynamic update of map markers and analysis based on filters

### Statistical Analysis
- Interactive box plot visualization using Plotly
- Comprehensive statistical summary including:
  - Mean, median, and standard deviation
  - Quartile distribution
  - Min/max values
  - Sample size metrics
- Visual comparison with target property values

### Spatial Analysis
- IDW (Inverse Distance Weighting) interpolation
- Detailed weight calculation process
- Percentage-based contribution analysis
- Predicted vs. actual price comparison

## 📊 Data Requirements

The system requires a CSV file (`warehouse_data.csv`) with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| Address | string | Property location address |
| Latitude | float | Geographic latitude |
| Longitude | float | Geographic longitude |
| Total Area (m²) | float | Total property area |
| Price | float | Property price in EUR (€) |
| Price per m² | float | Unit price in EUR (€) |

**Note**: The first row in the CSV file is considered as the target property for evaluation.

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd warehouse-evaluation
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

Launch the application using Streamlit:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501` by default.

## 📝 Usage Guidelines

1. **Data Preparation**
   - Ensure your CSV file follows the required format
   - Place the target property as the first entry
   - Verify all numerical values are properly formatted

2. **Filtering**
   - Use the sidebar controls to adjust search parameters
   - Distance filter: 0-50km radius from target property
   - Area filter: Adjustable tolerance range based on target property size

3. **Analysis**
   - Minimum 3 comparison properties required for IDW calculation
   - All monetary values are in EUR (€)
   - Statistical analysis updates automatically with filter changes

## 🛠 Technical Stack

- **Frontend**: Streamlit
- **Mapping**: Folium, streamlit-folium
- **Data Processing**: Pandas
- **Spatial Calculations**: GeoPy
- **Visualization**: Plotly
- **Statistical Analysis**: Native Python

## 📈 Performance Considerations

- Optimized for datasets with up to 1000 properties
- Caching implemented for data loading operations
- Efficient spatial calculations using GeoPy

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 