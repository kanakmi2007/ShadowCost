# ShadowCost

### See the hidden impact before you build.

ShadowCost is a spatial intelligence platform for evaluating the potential social, environmental, mobility, and infrastructure impacts of urban interventions before implementation.

It combines geospatial data, network analysis, spatial intersection modelling, scenario comparison, and AI-assisted synthesis into a single interactive workflow for exploring infrastructure decisions.

---

## Overview

Urban infrastructure decisions can affect more than the physical area where they are implemented.

A proposed road alignment or development footprint may interact with surrounding residential areas, commercial assets, green spaces, buildings, and transportation networks.

ShadowCost makes these relationships easier to explore by connecting a proposed intervention with its surrounding spatial context and translating the resulting analysis into measurable impact indicators.

The platform is designed around four primary impact dimensions:

| Dimension | What ShadowCost Evaluates |
|---|---|
| Social Exposure | Estimated population and residential exposure within the intervention context |
| Environmental Impact | Green-area and canopy effects associated with the intervention |
| Mobility Impact | Additional travel distance, rerouting, and peak-hour travel effects |
| Infrastructure Impact | Existing structures and spatial assets intersecting the intervention |

---

## Key Features

### Location-Based Spatial Analysis

Enter an urban location and generate a surrounding analysis area using geocoding and spatial buffering.

ShadowCost supports predefined locations as well as geocoded location queries.

### Interactive Intervention Design

Define the proposed intervention directly on an interactive map.

The current workflow supports:

- Road alignments
- Development footprints
- Corridor-width configuration
- Spatial geometry editing
- Intervention reset and re-analysis

### Geospatial Impact Engine

The impact engine evaluates the relationship between the proposed geometry and surrounding spatial features.

It calculates metrics related to:

- Population exposure
- Residential structures
- Commercial assets
- Green areas
- Canopy effects
- Affected infrastructure
- Travel impact
- Network-related changes

### Composite Shadow Impact Index

The calculated impact dimensions are combined into a normalized **0–100 Shadow Impact Index**.

The index provides a compact representation of the modelled impact profile while the underlying dimensions remain available for inspection.

### Interactive Spatial Visualization

ShadowCost uses interactive maps to visualize:

- Analysis boundaries
- Existing spatial assets
- Proposed intervention geometry
- Residential areas
- Commercial areas
- Parks and green spaces
- Other relevant urban features

### Scenario Comparison

Two intervention scenarios can be stored and compared.

The comparison view evaluates metrics including:

- People affected
- Green area affected
- Added peak travel
- Shadow Impact Index

This allows users to examine the trade-offs between alternative intervention configurations.

### AI-Assisted Impact Briefing

ShadowCost can generate a concise analytical briefing based on the calculated spatial metrics.

The AI synthesis considers:

- Location
- Intervention type
- People affected
- Green-area impact
- Travel impact
- Affected assets
- Shadow Impact Index

If an OpenAI API key is not provided, the application uses a built-in fallback synthesis.

### Executive Data Export

Analysis results can be exported in multiple formats:

- JSON spatial payload
- CSV impact metrics
- Executive briefing note

---

## How It Works

```text
LOCATION
   |
   v
GEOCODING & SPATIAL BUFFER
   |
   v
URBAN SPATIAL CONTEXT
   |
   +-- Residential Features
   +-- Commercial Features
   +-- Parks / Green Areas
   +-- Civic Structures
   +-- Street Network
   |
   v
INTERVENTION
   |
   +-- Road Alignment
   +-- Development Footprint
   |
   v
SPATIAL INTERSECTION ANALYSIS
   |
   +-- Social Exposure
   +-- Environmental Impact
   +-- Mobility Impact
   +-- Infrastructure Impact
   |
   v
SHADOW IMPACT INDEX
   |
   v
SCENARIO COMPARISON
   |
   v
AI-ASSISTED IMPACT BRIEF
   |
   v
JSON / CSV / EXECUTIVE EXPORT
```

---

## Application Workflow

### 01 — Overview

The landing workspace introduces ShadowCost and provides access to the spatial analysis workflow and predefined demonstration scenarios.

### 02 — Spatial Analysis

Select or geocode an urban location and inspect the surrounding spatial context.

### 03 — Intervention Setup

Draw the proposed intervention on the map and configure relevant parameters such as corridor width.

### 04 — Impact Analysis

Run the spatial analysis engine to calculate the resulting impact dimensions and Shadow Impact Index.

### 05 — Command Center

Review the calculated impact metrics, spatial context, and analytical briefing.

### 06 — Scenario Lab

Save and compare alternative scenarios using the same impact dimensions.

### 07 — Methodology

Review the underlying spatial workflow, impact dimensions, and calculation methodology.

### 08 — Executive Report

Generate and download structured analysis outputs in JSON and CSV formats and preview the executive briefing.

---

## Impact Model

ShadowCost currently evaluates four major dimensions.

### Social Exposure

The model estimates population exposure associated with residential features affected by the proposed intervention.

The analysis considers different residential feature types and derives an estimated affected population.

### Environmental Impact

The environmental analysis considers green areas and canopy-related effects associated with the intervention.

Relevant outputs include:

* Green area affected
* Green-cover change
* Estimated canopy effects
* Heat-exposure-related indicators

### Mobility Impact

The mobility model estimates changes associated with the proposed intervention.

Relevant outputs include:

* Average added travel distance
* Daily trips rerouted
* Peak-hour travel change
* Network detour effects

### Infrastructure Impact

The infrastructure dimension measures spatial interaction with existing urban assets.

Depending on the intervention, this can include affected:

* Residential structures
* Commercial structures
* Parks
* Other mapped assets

---

## Shadow Impact Index

The four impact dimensions contribute to a normalized:

**Composite Shadow Impact Index — 0 to 100**

The index is calculated from the modelled social, environmental, mobility, and infrastructure scores.

It is intended as a **decision-support metric** for comparing intervention scenarios rather than as a substitute for detailed engineering, environmental, traffic, or statutory planning studies.

---

## Spatial Data

ShadowCost uses OpenStreetMap-based spatial information together with locally generated urban feature layers.

The platform's spatial workflow includes:

* Location geocoding
* Spatial buffers
* OpenStreetMap map tiles
* Street-network data
* Building and urban feature geometries
* Green-space and park features
* Residential and commercial feature representations

The current demographic/urban feature layer is generated programmatically for analysis scenarios rather than representing a complete real-world demographic database.

---

## Network Analysis

ShadowCost includes NetworkX-based network analysis and GraphML network data.

The project contains:

```text
local_network.graphml
```

A separate utility, `fetch_data.py`, can retrieve a pedestrian street network from OpenStreetMap using OSMnx and save the resulting graph as GraphML.

The network layer supports the mobility-analysis workflow and provides a basis for modelling travel and rerouting effects.

---

## AI-Assisted Synthesis

ShadowCost includes an optional OpenAI-powered synthesis layer.

When an API key is available, the application uses the calculated impact metrics to generate a concise analytical briefing.

The synthesis is structured around:

1. Dominant modelled impact
2. Key social and environmental considerations
3. Potential mitigation strategies

The AI layer is designed to summarize calculated results rather than replace the underlying spatial analysis.

If no API key is configured, ShadowCost automatically falls back to a deterministic briefing generated from the available metrics.

---

## Scenario Comparison

ShadowCost supports two saved scenario slots:

```text
Scenario A
    |
    +-- People affected
    +-- Green area affected
    +-- Added peak travel
    +-- Shadow Impact Index

Scenario B
    |
    +-- People affected
    +-- Green area affected
    +-- Added peak travel
    +-- Shadow Impact Index
```

The Scenario Lab presents the resulting metrics together so that users can inspect the trade-offs between alternative intervention configurations.

---

## Quick Demo

ShadowCost includes predefined demonstration scenarios to make the application easier to explore without starting from an empty workspace.

Available examples include:

* Road Alignment — Saket, Delhi
* Building Footprint — Bandra West, Mumbai

The application also initializes a default demonstration scenario around Saket, New Delhi.

---

## Technology Stack

### Application

* Python
* Streamlit

### Geospatial Analysis

* GeoPandas
* Shapely
* OSMnx

### Interactive Mapping

* Folium
* Streamlit-Folium
* OpenStreetMap

### Network Analysis

* NetworkX
* GraphML

### Data Processing

* Pandas
* NumPy

### AI Synthesis

* OpenAI API

---

## Project Structure

```text
ShadowCost/
|
├── app.py
├── config.py
├── fetch_data.py
├── local_network.graphml
├── requirements.txt
├── .gitignore
|
├── components/
│   ├── landing.py
│   ├── location_selector.py
│   ├── intervention_setup.py
│   ├── dashboard.py
│   ├── comparison.py
│   ├── methodology.py
│   └── exporter.py
|
└── core/
    ├── geocoding.py
    ├── demographics.py
    ├── impact_engine.py
    ├── ai_synthesizer.py
    └── scenario_manager.py
```

---

## Getting Started

### Prerequisites

Make sure Python is installed on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/kanakmi2007/ShadowCost.git
cd ShadowCost
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will start locally at:

```text
http://localhost:8501
```

---

## Optional AI Configuration

AI-assisted synthesis is optional.

You can provide an OpenAI API key through the application's configuration interface.

The application accepts the key through the Streamlit sidebar and also supports the `OPENAI_API_KEY` environment variable.

Without an API key, ShadowCost uses its built-in fallback impact briefing.

---

## Generating Network Data

The project includes `fetch_data.py` for downloading a pedestrian street network from OpenStreetMap using OSMnx.

Run:

```bash
python fetch_data.py
```

The generated network is stored as:

```text
local_network.graphml
```

---

## Example Use Cases

ShadowCost can support exploratory analysis of:

* Urban road alignments
* Development footprints
* Corridor planning
* Streetscape interventions
* Mobility infrastructure
* Public-space interventions
* Green-space-sensitive development
* Early-stage infrastructure planning

---

## Design Philosophy

ShadowCost follows an evidence-first workflow.

Instead of treating the final score as the entire analysis:

```text
Data
  |
  v
Spatial Relationships
  |
  v
Calculated Metrics
  |
  v
Impact Dimensions
  |
  v
Shadow Impact Index
  |
  v
Decision Insights
```

The goal is to keep the calculated metrics visible so that the final impact assessment can be understood in terms of the underlying spatial relationships.

---

## Limitations

ShadowCost is an exploratory decision-support prototype.

Its outputs depend on:

* available spatial data
* geocoding results
* completeness of network data
* assumptions within the impact model
* generated urban feature representations
* model parameters used for scenario calculations

The demographic and urban feature layer currently used by the prototype is generated programmatically for scenario analysis and should not be interpreted as authoritative census or planning data.

Similarly, the Shadow Impact Index should not be treated as a statutory planning score or a substitute for professional engineering, traffic, environmental, or social-impact assessment.

---

## Future Scope

Potential extensions include:

* Integration with richer real-world demographic datasets
* More detailed city-scale spatial layers
* Expanded environmental indicators
* More advanced traffic and network simulation
* Additional intervention types
* Multi-scenario optimization
* Historical intervention benchmarking
* More detailed mitigation modelling
* Real-time urban data integration
* Scalable deployment for civic planning workflows

---

## Project Vision

> **See the hidden impact before you build.**

ShadowCost aims to make early-stage infrastructure analysis more transparent by connecting spatial evidence, measurable impact indicators, scenario comparison, and decision-oriented synthesis in one workflow.

---

## Team

ShadowCost was developed as a hackathon project focused on:

**Geospatial Intelligence · Urban Planning · Network Analysis · Spatial Impact Analysis · AI-Assisted Decision Support**

---

## License

This project is currently intended as a hackathon and prototype project.

An explicit open-source license can be added if the project is later distributed under a specific license.

```

