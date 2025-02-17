# ITS Data Visualization Dashboard

A Streamlit dashboard for visualizing and analyzing academic data from ITS AI & Data Science course.

## Features

- **Lesson Distribution**: Visualize teaching hours distribution across instructors
  - Pie chart with total hours
  - Bar chart showing individual instructor hours
  - Toggle between 1st and 2nd year data

- **Academic Performance Analysis**:
  - Student grade averages with visualizations
  - Teacher grade distributions
  - Attendance tracking with critical threshold indicators
  - Individual student report cards

- **Performance Metrics**:
  - Top and bottom performers
  - Attendance champions
  - Performance/attendance ratio analytics

## Installation

1. Clone this repository
2. Install requirements:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run main.py
```

## Data Requirements

The application expects the following data files in the `./data` directory:
- `Calendario AI&DS - biennio 2023-25 - Calendario 1° anno.csv`
- `Calendario AI&DS - biennio 2023-25 - Calendario 2° anno.csv`
- `Valutazioni_Presenze.xlsx`

## Docker Support

For Docker deployment, refer to `README.Docker.md`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
