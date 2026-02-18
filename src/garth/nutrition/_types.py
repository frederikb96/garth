from __future__ import annotations

from dataclasses import field

from pydantic.dataclasses import dataclass


@dataclass
class FoodMetaData:
    food_name: str
    food_id: str | None = None
    food_type: str | None = None
    brand_name: str | None = None
    source: str | None = None
    region_code: str | None = None
    language_code: str | None = None
    image_uuid: str | None = None


@dataclass
class NutritionContent:
    serving_id: str | None = None
    serving_unit: str | None = None
    number_of_units: float | None = None
    calories: float | None = None
    carbs: float | None = None
    protein: float | None = None
    fat: float | None = None
    fiber: float | None = None
    sugar: float | None = None
    added_sugars: float | None = None
    saturated_fat: float | None = None
    monounsaturated_fat: float | None = None
    polyunsaturated_fat: float | None = None
    trans_fat: float | None = None
    cholesterol: float | None = None
    sodium: float | None = None
    potassium: float | None = None
    vitamin_a: float | None = None
    vitamin_c: float | None = None
    vitamin_d: float | None = None
    calcium: float | None = None
    iron: float | None = None
    unit_has_serving: bool | None = None


@dataclass
class MacroGoals:
    calories: float | None = None
    adjusted_calories: float | None = None
    carbs: float | None = None
    adjusted_carbs: float | None = None
    fat: float | None = None
    adjusted_fat: float | None = None
    protein: float | None = None
    adjusted_protein: float | None = None


@dataclass
class Meal:
    meal_id: int
    meal_name: str
    display_order: int
    start_time: str | None = None
    end_time: str | None = None
    goals: MacroGoals | None = None


@dataclass
class LoggedFood:
    id: str | None = None
    log_id: str | None = None
    log_timestamp: str | None = None
    log_source: str | None = None
    log_category: str | None = None
    serving_qty: float | None = None
    food_meta_data: FoodMetaData | None = None
    selected_nutrition_content: NutritionContent | None = None
    nutrition_contents: list[NutritionContent] = field(default_factory=list)
    food_images: list[dict] = field(default_factory=list)
    is_favorite: bool | None = None


@dataclass
class MealDetail:
    meal: Meal
    meal_nutrition_content: NutritionContent | None = None
    meal_nutrition_goals: MacroGoals | None = None
    logged_foods: list[LoggedFood] = field(default_factory=list)


@dataclass
class DailyNutritionSummary:
    calories: float | None = None
    carbs: float | None = None
    fat: float | None = None
    protein: float | None = None
    calories_percentage: float | None = None
