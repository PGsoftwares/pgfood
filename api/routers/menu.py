import random
from typing import List, Optional
from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile
from apps.partners.models import AddonGroup, FoodItem, MenuCategory
from ..schemas import (
    AddonGroupCreateRequest, AvailabilityToggleRequest,
    CategoryUpdateRequest, FoodItemUpdateRequest, GenericResponse
)

router = APIRouter(prefix="/menu", tags=["5. Food Menu & Customizations"])


# Categories
@router.get("/categories")
def get_categories():
    """5.1 Get Menu Categories."""
    cats = MenuCategory.objects.all()
    if cats.exists():
        return [
            {
                "id": c.category_id,
                "name": c.name,
                "image": c.image_url or "https://cdn.pgpartner.com/categories/default.png",
                "itemCount": c.item_count,
                "status": c.status
            }
            for c in cats
        ]
    return [
        {"id": "CAT-1", "name": "Main Course", "image": "https://cdn.pgpartner.com/categories/main_course.png", "itemCount": 18, "status": True},
        {"id": "CAT-2", "name": "Biryani & Rice", "image": "https://cdn.pgpartner.com/categories/biryani.png", "itemCount": 8, "status": True}
    ]


@router.post("/categories", status_code=201)
async def create_category(
    name: str = Form(...),
    image: Optional[UploadFile] = File(None),
    status: bool = Form(True)
):
    """5.2 Create Menu Category."""
    cat_id = f"CAT-{random.randint(6, 99)}"
    img_url = f"https://cdn.pgpartner.com/categories/{name.lower().replace(' ', '_')}.png"

    MenuCategory.objects.create(
        category_id=cat_id,
        name=name,
        image_url=img_url,
        item_count=0,
        status=status
    )

    return {
        "success": True,
        "category": {
            "id": cat_id,
            "name": name,
            "image": img_url,
            "itemCount": 0,
            "status": status
        }
    }


@router.put("/categories/{categoryId}", response_model=GenericResponse)
def update_category(categoryId: str, payload: CategoryUpdateRequest):
    """5.3 Update Menu Category."""
    cat = MenuCategory.objects.filter(category_id=categoryId).first()
    if cat:
        cat.name = payload.name
        cat.status = payload.status
        cat.save()
    return GenericResponse(success=True, message="Category updated successfully")


@router.delete("/categories/{categoryId}", response_model=GenericResponse)
def delete_category(categoryId: str):
    """5.4 Delete Menu Category."""
    MenuCategory.objects.filter(category_id=categoryId).delete()
    return GenericResponse(success=True, message="Category deleted successfully")


# Items
@router.get("/items")
def get_food_items(
    category: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """5.5 Get Food Items."""
    qs = FoodItem.objects.all()
    if category:
        qs = qs.filter(category__icontains=category)
    if type:
        qs = qs.filter(food_type=type)
    if search:
        qs = qs.filter(name__icontains=search)

    if qs.exists():
        return [
            {
                "id": item.item_id,
                "name": item.name,
                "description": item.description,
                "category": item.category,
                "type": item.food_type,
                "price": item.price,
                "prepTimeMinutes": item.prep_time_minutes,
                "available": item.available,
                "rating": item.rating,
                "image": item.image_url
            }
            for item in qs
        ]

    return [
        {
            "id": "FOOD-101",
            "name": "Paneer Butter Masala",
            "description": "Rich tomato butter gravy with soft cottage cheese cubes",
            "category": "Main Course",
            "type": "veg",
            "price": 280.0,
            "prepTimeMinutes": 15,
            "available": True,
            "rating": 4.8,
            "image": "https://cdn.pgpartner.com/dishes/paneer_butter_masala.jpg"
        }
    ]


@router.post("/items", status_code=201)
async def add_food_item(
    name: str = Form(...),
    description: str = Form(""),
    category: str = Form("Main Course"),
    type: str = Form("veg"),
    price: float = Form(...),
    prepTimeMinutes: int = Form(15),
    image: Optional[UploadFile] = File(None),
    available: bool = Form(True)
):
    """5.6 Add Food Item."""
    new_id = f"FOOD-{random.randint(102, 999)}"
    img_url = f"https://cdn.pgpartner.com/dishes/{name.lower().replace(' ', '_')}.jpg"

    FoodItem.objects.create(
        item_id=new_id,
        name=name,
        description=description,
        category=category,
        food_type=type,
        price=price,
        prep_time_minutes=prepTimeMinutes,
        available=available,
        image_url=img_url
    )

    return {
        "success": True,
        "item": {
            "id": new_id,
            "name": name,
            "price": price,
            "available": available,
            "imageUrl": img_url
        }
    }


@router.put("/items/{itemId}", response_model=GenericResponse)
def update_food_item(itemId: str, payload: FoodItemUpdateRequest):
    """5.7 Update Food Item."""
    item = FoodItem.objects.filter(item_id=itemId).first()
    if item:
        item.name = payload.name
        item.price = payload.price
        item.description = payload.description or ""
        item.category = payload.category
        item.available = payload.available
        item.save()
    return GenericResponse(success=True, message="Food item updated successfully")


@router.patch("/items/{itemId}/availability")
def toggle_item_availability(itemId: str, payload: AvailabilityToggleRequest):
    """5.8 Toggle Item Stock Availability."""
    item = FoodItem.objects.filter(item_id=itemId).first()
    if item:
        item.available = payload.available
        item.save()

    msg = "Item marked Available" if payload.available else "Item marked Out of Stock"
    return {
        "success": True,
        "itemId": itemId,
        "available": payload.available,
        "message": msg
    }


@router.delete("/items/{itemId}", response_model=GenericResponse)
def delete_food_item(itemId: str):
    """5.9 Delete Food Item."""
    FoodItem.objects.filter(item_id=itemId).delete()
    return GenericResponse(success=True, message="Item removed from menu")


# Add-on Customizations
@router.get("/addons")
def get_addons():
    """5.10 Get Customization Add-on Groups."""
    groups = AddonGroup.objects.all()
    if groups.exists():
        return [
            {
                "id": g.group_id,
                "groupName": g.group_name,
                "required": g.required,
                "minSelection": g.min_selection,
                "maxSelection": g.max_selection,
                "options": g.options
            }
            for g in groups
        ]
    return [
        {
            "id": "GRP-1",
            "groupName": "Choose Portion Size (Variant)",
            "required": True,
            "minSelection": 1,
            "maxSelection": 1,
            "options": [
                {"id": "OPT-1", "name": "Half Portion", "price": 0.0},
                {"id": "OPT-2", "name": "Full Portion", "price": 140.0}
            ]
        }
    ]


@router.post("/addons", status_code=201)
def create_addon_group(payload: AddonGroupCreateRequest):
    """5.11 Create Add-on Group."""
    group_id = f"GRP-{random.randint(2, 99)}"
    options_data = [opt.model_dump() for opt in payload.options]

    AddonGroup.objects.create(
        group_id=group_id,
        group_name=payload.groupName,
        required=payload.required,
        min_selection=payload.minSelection,
        max_selection=payload.maxSelection,
        options=options_data
    )

    return {
        "success": True,
        "id": group_id,
        "message": "Add-on group created successfully"
    }


@router.delete("/addons/{groupId}", response_model=GenericResponse)
def delete_addon_group(groupId: str):
    """5.12 Delete Add-on Group."""
    AddonGroup.objects.filter(group_id=groupId).delete()
    return GenericResponse(success=True, message="Customization group removed")
