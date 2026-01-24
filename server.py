from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal

app = FastAPI(title="Calculator API")


class CalculatorRequest(BaseModel):
    operation: Literal["add", "subtract", "multiply", "divide"]
    a: float
    b: float


class CalculatorResponse(BaseModel):
    result: float


@app.post("/calculate", response_model=CalculatorResponse)
async def calculate(request: CalculatorRequest):
    """Perform a calculation based on the operation type."""
    try:
        if request.operation == "add":
            result = request.a + request.b
        elif request.operation == "subtract":
            result = request.a - request.b
        elif request.operation == "multiply":
            result = request.a * request.b
        elif request.operation == "divide":
            if request.b == 0:
                raise HTTPException(
                    status_code=400, detail="Division by zero is not allowed"
                )
            result = request.a / request.b
        else:
            raise HTTPException(
                status_code=400, detail=f"Unknown operation: {request.operation}"
            )

        return CalculatorResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
