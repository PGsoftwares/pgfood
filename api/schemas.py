from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------
# 1. Auth Schemas
# ---------------------------
class PartnerLoginRequest(BaseModel):
    identifier: str = Field(..., description="Registered mobile number or email")
    password: str = Field(..., description="Account password")


class PartnerInfo(BaseModel):
    id: str
    name: str
    mobile: str
    email: str
    restaurantId: str
    status: str


class PartnerLoginResponse(BaseModel):
    success: bool
    token: str
    partner: PartnerInfo


class ForgotPasswordRequest(BaseModel):
    identifier: str


class ForgotPasswordResponse(BaseModel):
    success: bool
    message: str
    otpSessionId: str
    expiresInSeconds: int = 60


class VerifyOtpRequest(BaseModel):
    otpSessionId: str
    otp: str


class VerifyOtpResponse(BaseModel):
    success: bool
    verificationToken: str
    message: str


class ResetPasswordRequest(BaseModel):
    verificationToken: str
    newPassword: str
    confirmPassword: str


class GenericResponse(BaseModel):
    success: bool
    message: str


# ---------------------------
# 2. Registration Schemas
# ---------------------------
class OwnerDetailsRequest(BaseModel):
    ownerName: str
    mobileNumber: str
    email: str
    password: str


class OwnerDetailsResponse(BaseModel):
    success: bool
    registrationId: str
    nextStep: str = "restaurant_details"


class AddressDetailsRequest(BaseModel):
    registrationId: str
    address: str
    area: str
    city: str
    state: str
    pincode: str
    landmark: Optional[str] = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class BankDetailsRequest(BaseModel):
    registrationId: str
    accountHolderName: str
    accountNumber: str
    confirmAccountNumber: str
    ifscCode: str
    bankName: str
    branch: str


class SubmitRegistrationRequest(BaseModel):
    registrationId: str
    termsAccepted: bool


# ---------------------------
# 3. Outlet & Dashboard Schemas
# ---------------------------
class OutletStatusRequest(BaseModel):
    isOnline: bool
    reason: Optional[str] = None
    resumeAt: Optional[str] = None


# ---------------------------
# 4. Orders Schemas
# ---------------------------
class AcceptOrderRequest(BaseModel):
    preparationMinutes: int = 20


class RejectOrderRequest(BaseModel):
    reason: str


class PrepTimeRequest(BaseModel):
    additionalMinutes: int = 10


class HandoverRequest(BaseModel):
    pickupOtp: str


# ---------------------------
# 5. Menu Schemas
# ---------------------------
class CategoryUpdateRequest(BaseModel):
    name: str
    status: bool = True


class FoodItemUpdateRequest(BaseModel):
    name: str
    price: float
    description: Optional[str] = ""
    category: str
    available: bool = True


class AvailabilityToggleRequest(BaseModel):
    available: bool


class AddonOption(BaseModel):
    name: str
    price: float


class AddonGroupCreateRequest(BaseModel):
    groupName: str
    required: bool = False
    minSelection: int = 0
    maxSelection: int = 1
    options: List[AddonOption]


# ---------------------------
# 6. Offers Schemas
# ---------------------------
class CreateOfferRequest(BaseModel):
    name: str
    code: str
    discountType: str = "Percentage"
    discountValue: float
    minOrder: float = 0.0
    startDate: str
    endDate: str


# ---------------------------
# 7. Timings Schemas
# ---------------------------
class WorkingHoursUpdateRequest(BaseModel):
    workingDays: Dict[str, bool]
    openingTime: str
    closingTime: str
    hasBreakTime: bool = False
    breakStartTime: Optional[str] = None
    breakEndTime: Optional[str] = None


# ---------------------------
# 9. Reviews Schemas
# ---------------------------
class ReviewReplyRequest(BaseModel):
    replyText: str


# ---------------------------
# 11. Profile Schemas
# ---------------------------
class ProfileUpdateRequest(BaseModel):
    restaurantName: Optional[str] = None
    ownerName: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


# ---------------------------
# 13. Settings Schemas
# ---------------------------
class ChangePasswordRequest(BaseModel):
    currentPassword: str
    newPassword: str
    confirmPassword: str


class NotificationPreferencesRequest(BaseModel):
    orderAlertsSound: bool = True
    soundVolume: str = "High"
    payoutWhatsappUpdates: bool = True
    marketingOffers: bool = False


class LogoutRequest(BaseModel):
    deviceToken: Optional[str] = None
