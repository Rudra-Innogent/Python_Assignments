import pandas as pd
import csv
from typing import List, Dict
from datetime import datetime
from fastapi import UploadFile, HTTPException
import io


async def process_csv_file(file: UploadFile) -> List[Dict]:
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    try:
        # Read CSV file content
        contents = await file.read()

        # Use pandas to parse CSV
        df = pd.read_csv(io.BytesIO(contents))

        # Convert to list of dictionaries
        records = df.to_dict('records')

        # Validate and format data
        processed_records = []
        for record in records:
            try:
                processed_record = {
                    'name': str(record['name']),
                    'email': str(record['email']),
                    'department': str(record['department']),
                    'salary': float(record['salary']),
                    'joinDate': pd.to_datetime(record['joinDate']).to_pydatetime()
                }
                processed_records.append(processed_record)
            except Exception as e:
                print(f"Error processing record: {record}, Error: {e}")
                continue

        return processed_records
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")
    finally:
        await file.close()


def create_csv_response(data: List[Dict], filename: set = "export.csv"):
    if not data:
        return ""

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    return output.getvalue()


def create_excel_response(data: List[Dict], filename: str = "export.xlsx"):
    if not data:
        return b""

    df = pd.DataFrame(data)

    # Create Excel in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')

    output.seek(0)
    return output.getvalue()