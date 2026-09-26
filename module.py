from pydantic import BaseModel


# Request model for finding/deleting a BIN
class BinRequest(BaseModel):
    bin_iin: str


# Request model for creating/updating a BIN
class BinCreateRequest(BaseModel):
    bin_iin: str
    network: str
    card_type: str
    card_category: str
    issuer: str


# Request model for auto-suggestion
class SuggestionRequest(BaseModel):
    query: str