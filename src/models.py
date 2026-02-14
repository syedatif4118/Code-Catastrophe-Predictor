"""
Autonomous Alpha - Pydantic Models
Strict typing for all data structures in the trading system.
"""
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TradingAction(str, Enum):
    """Trading action enumeration."""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class MarketData(BaseModel):
    """Market data snapshot."""
    symbol: str
    timestamp: datetime
    price: Decimal = Field(gt=0, description="Current market price")
    volume: int = Field(ge=0)
    rsi_14: Optional[float] = Field(None, ge=0, le=100, description="14-period RSI")

    @field_validator('price', mode='before')
    @classmethod
    def convert_price(cls, v):
        return Decimal(str(v))


class TradeSignal(BaseModel):
    """Trading signal with explainable rationale."""
    symbol: str
    action: TradingAction
    quantity: int = Field(gt=0)
    rationale: str = Field(description="Human-readable explanation of signal")
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    strategy_name: str
    indicators: dict[str, float] = Field(default_factory=dict)

    class Config:
        use_enum_values = True


class RiskCheckResult(BaseModel):
    """Result of risk validation."""
    approved: bool
    signal: TradeSignal
    violations: list[str] = Field(default_factory=list)
    buying_power_available: Decimal
    position_size_percent: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('buying_power_available', mode='before')
    @classmethod
    def convert_buying_power(cls, v):
        return Decimal(str(v))


class OrderResult(BaseModel):
    """Execution result."""
    order_id: Optional[str] = None
    symbol: str
    action: TradingAction
    quantity: int
    filled_price: Optional[Decimal] = None
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None

    @field_validator('filled_price', mode='before')
    @classmethod
    def convert_price(cls, v):
        if v is None:
            return None
        return Decimal(str(v))

    class Config:
        use_enum_values = True


class AuditLog(BaseModel):
    """Glass Box audit log entry."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    state: str = Field(description="Current state in state machine")
    inputs: dict = Field(description="Inputs to this state")
    outputs: dict = Field(description="Outputs from this state")
    rationale: str = Field(description="Explanation of transition")
    duration_ms: Optional[float] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: str(v),
        }
