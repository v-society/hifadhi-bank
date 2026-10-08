from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import auth
from routes import client
from routes.user import User

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class CardRequest(BaseModel):
    card_number: str


class PinRequest(BaseModel):
    card_number: str
    pin: str


class TransactionRequest(PinRequest):
    amount: float


@app.get("/")
def home():
    return {"message": "Hifadhi Banking API"}


@app.post("/card-number")
def receive_card_number(request: CardRequest):
    if not auth.check_card_number(request.card_number):
        return {"accepted": False, "message": "Card number not recognized"}

    return {"accepted": True, "message": "Card accepted"}


@app.post("/authenticate")
def authenticate_card(request: PinRequest):
    account = User.authenticate(request.card_number.strip(), request.pin)
    if account is None:
        return {"authenticated": False, "message": "Incorrect PIN"}

    return {"authenticated": True, "name": account["name"]}


@app.post("/balance")
def check_balance(request: PinRequest):
    account = User.authenticate(request.card_number.strip(), request.pin)
    if account is None:
        return {"success": False, "message": "Card or PIN is invalid"}

    return {"success": True, "balance": account["balance"]}


def process_transaction(request: TransactionRequest, transaction_type: str):
    account = User.authenticate(request.card_number.strip(), request.pin)
    if account is None:
        return {"success": False, "message": "Card or PIN is invalid"}
    if request.amount <= 0:
        return {"success": False, "message": "Amount must be greater than zero"}

    if transaction_type == "deposit":
        completed = client.deposit(account["account_number"], request.amount)
    elif transaction_type == "withdraw":
        completed = client.withdraw(account["account_number"], request.amount)
    else:
        return {"success": False, "message": "Unknown transaction"}

    if not completed:
        return {"success": False, "message": "Insufficient funds"}

    updated_account = next(
        user
        for user in User.load_users()
        if str(user.get("card_number")) == request.card_number.strip()
    )
    return {
        "success": True,
        "message": f"{transaction_type.title()} successful",
        "balance": updated_account["balance"],
    }


@app.post("/transactions/{transaction_type}")
def transact(transaction_type: str, request: TransactionRequest):
    return process_transaction(request, transaction_type)