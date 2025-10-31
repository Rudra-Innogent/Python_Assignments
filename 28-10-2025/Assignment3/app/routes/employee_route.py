from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse, Response
from typing import List, Optional
from datetime import datetime
import io

from app.schemas.employee_schema import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.database.database import prisma
from app.core.file_handler import create_excel_response, process_csv_file, create_csv_response

router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"]
)


@router.post("/upload-csv", status_code=201)
async def upload_csv(file: UploadFile = File(...)):
    records = await process_csv_file(file)

    if not records:
        raise HTTPException(
            status_code=400,
            detail=f"No Valid Records Found In CSV"
        )

    created_count = 0
    failed_records = []

    for record in records:
        try:
            await prisma.employee.create(data=record)
            created_count += 1
        except Exception as e:
            failed_records.append({
                "record": record,
                "error": str(e)
            })

    return {
        "message": f"Successfully imported {created_count} records",
        "total_records": len(records),
        "created": created_count,
        "failed": len(failed_records),
        "failed_records": failed_records[:10]  # Show first 10 failures
    }


@router.post("/", status_code=201)
async def create_employee(employee: EmployeeCreate):
    try:
        existing = await prisma.employee.find_unique(where={"email": employee.email})

        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Employee Already Exits"
            )

        new_employee = await prisma.employee.create(
            data={
                "name": employee.name,
                "email": employee.email,
                "department": employee.department,
                "salary": employee.salary,
                "joinDate": employee.joinDate
            }
        )
        return new_employee

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/download/csv")
async def download_csv():
    employees = await prisma.employee.find_many()

    data = []
    for emp in employees:
        data.append({
            "id": emp.id,
            "name": emp.name,
            "department": emp.department,
            "email": emp.email,
            "salary": emp.salary,
            "joinDate": emp.joinDate.strftime("%Y-%m-%d"),
            "createdAt": emp.createdAt.strftime("%Y-%m-%d %H:%M:%S")
        }
        )

    csv_content = create_csv_response(data)

    # Return as downloadable file
    return StreamingResponse(
        io.StringIO(csv_content),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )


@router.get("/download/xlsx")
async def download_xlsx():
    employees = await prisma.employee.find_many()

    if not employees:
        raise HTTPException(status_code=404, detail="No data found")

    # Convert to dictionaries
    data = []
    for emp in employees:
        data.append({
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "department": emp.department,
            "salary": emp.salary,
            "joinDate": emp.joinDate.strftime("%Y-%m-%d"),
            "createdAt": emp.createdAt.strftime("%Y-%m-%d %H:%M:%S")
        })

    # Create Excel content
    excel_content = create_excel_response(data)

    # Return as downloadable file
    return Response(
        content=excel_content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        }
    )


