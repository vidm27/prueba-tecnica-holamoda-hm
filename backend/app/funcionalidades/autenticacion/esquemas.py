from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiJ9.firma',
         'token_type': 'bearer',
         'expira_en_minutos': 60}})
    access_token: str
    token_type: str = "bearer"
    expira_en_minutos: int
