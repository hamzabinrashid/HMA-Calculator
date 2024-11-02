
# HMA Calculator


## Table of Contents

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoint](#api-endpoint)
6. [Source Code Structure](#source-code-structure)
7. [Additional Notes](#additional-notes)

## Overview

This application performs calculations on input data from an uploaded Excel file (`hma.xls`). Based on the values in column C, it calculates additional columns and exports the result to a CSV file. The calculations involve computing average gains, losses, and an indicator value derived from Excel-like formulas.

## Requirements

- Python 3.7 or higher
- `Flask` and `pandas` libraries

External dependencies are listed in `requirements.txt`.

## Installation

1. Clone the repository or download the files.
2. Navigate to the project directory.
3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:

   ```bash
   python main.py
   ```

   The server will start on `http://127.0.0.1:8000`.

2. Use an API testing tool (like Postman) or `curl` to upload the Excel file (`hma.xls`), and the application will return a processed CSV file with calculated columns.

## API Endpoint

### `/process` (POST)

This endpoint processes an uploaded Excel file.

- **URL:** `http://127.0.0.1:8000/process`
- **Method:** POST
- **Form Data:**
  - `file`: The uploaded Excel file in `.xls` or `.xlsx` format.
- **Response:** Returns a CSV file with calculated columns.

#### Example Usage with `curl`:

```bash
curl -X POST -F "file=@path/to/hma.xls" http://127.0.0.1:8000/process -o processed_file.csv
```

#### Expected Output

A CSV file with columns B, C and D, E, F, G, H, I, J (calculated columns).

## Source Code Structure

- `app.py`: The main Flask application file that defines the API endpoint.
- `calculate_columns`: A function that applies formulas to compute values for columns D, E, F, G, H, I, and J based on column C data.
- `allowed_file`: Helper function to validate file extension.
- `requirements.txt`: Specifies required libraries.

### Code Explanation

1. **File Upload and Validation:** The `/process` endpoint accepts and validates file uploads.
2. **Data Processing with `calculate_columns`:** Reads the Excel file, applies calculations, and stores results in new columns (D-J).
3. **Return CSV Output:** Exports the DataFrame to a CSV file and sends it as a downloadable response.

## Additional Notes

- **Error Handling:** Basic error handling is implemented; errors during file processing return a 500 status.
- **Temporary Files:** The application temporarily stores files in `./temp` and removes them post-processing (optional).

---
