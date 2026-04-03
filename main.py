from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vanna_service import NL2SQLService


app = FastAPI(
    title="NL2SQL API",
    description="Convert natural language questions into SQL queries",
    version="1.0"
)


class QuestionRequest(BaseModel):
    question: str


service = NL2SQLService("clinic.db")


@app.get("/")
def root():
    return {"message": "NL2SQL API is running"}


@app.post("/chat")
def chat(request: QuestionRequest):

    try:

        question = request.question

        sql_query = service.generate_sql(question)

        result = service.run_query(sql_query)

        return {
            "question": question,
            "sql": sql_query,
            "result": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )