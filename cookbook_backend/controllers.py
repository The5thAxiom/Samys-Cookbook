from cookbook_backend import db
from cookbook_backend.models import *

def addFullRecipe(newRecipeFull):
    # adding the contributor (if it doesn't exist already)
    contributor = Contributor.query.filter_by(name = newRecipeFull["contributor_name"]).first()
    if contributor is None:
        contributor = Contributor(**{
            "name": newRecipeFull["contributor_name"]
        })
        db.session.add(contributor)
        db.session.commit()

    newRecipe = Recipe(**{
        "name": newRecipeFull["name"],
        "prep_time": newRecipeFull["prep_time"],
        "description": newRecipeFull["description"],
        "difficulty": newRecipeFull["difficulty"],
        "contributor_id": contributor.id,
        "vegetarian": newRecipeFull["vegetarian"],
        "quantity": newRecipeFull["quantity"],
        "unit": newRecipeFull["unit"]
    })
    db.session.add(newRecipe)
    db.session.commit()

    for step in newRecipeFull["recipe_steps"]:
        db.session.add(Recipe_Steps(**{
            "recipe_id": newRecipe.id,
            "serial_number": step["serial_number"],
            "instruction": step["instruction"]
        }))
    db.session.commit()

    for tag in newRecipeFull["recipe_tags"]:
        db.session.add(Tags(**{
            "recipe_id": newRecipe.id,
            "name": tag["name"]
        }))
    db.session.commit()

    # add all the ingredients (if they don't exist already)
    for ingredient in newRecipeFull["recipe_ingredients"]:
        newIngredient = Ingredient.query.filter_by(english_name = ingredient["english_name"]).first()
        if newIngredient is None:
            newIngredient = Ingredient(**{
                "english_name": ingredient["english_name"],
                "hindi_name_latin": ingredient["hindi_name_latin"],
                "hindi_name_devnagari": ingredient["hindi_name_devnagari"]
            })
            db.session.add(newIngredient)
            db.session.commit()

        db.session.add(Recipe_Ingredients(**{
                "recipe_id": newRecipe.id,
                "ingredient_id": newIngredient.id,
                "quantity": ingredient["quantity"],
                "unit": ingredient["unit"]
        }))
    db.session.commit()


def getRecipeById(id: int) -> Recipe | None:
    return Recipe.query.filter_by(id = id).first()

def getRecipeMeta(recipe: Recipe) -> dict:
    recipe = recipe.__dict__
    recipe.pop('_sa_instance_state')
    return recipe

def getRecipeIngredients(recipe: Recipe) -> dict:
    recipeIngredients = []
    for recipe_ingredient in Recipe_Ingredients.query.filter_by(recipe_id = recipe.id):
        ingredient = Ingredient.query.filter_by(id = recipe_ingredient.ingredient_id).first()
        recipeIngredients.append({
            "english_name": ingredient.english_name,
            "hindi_name_latin": ingredient.hindi_name_latin,
            "hindi_name_devnagari": ingredient.hindi_name_devnagari,
            "quantity": recipe_ingredient.quantity,
            "unit": recipe_ingredient.unit
        })
    return recipeIngredients

def getRecipeTags(recipe: Recipe) -> list[dict]:
    return [
        {
            "name": tag.name
        } for tag in Tags.query.filter_by(recipe_id = recipe.id)
    ]

def getRecipeSteps(recipe: Recipe) -> list[dict]:
    return [
        {
            "serial_number": step.serial_number,
            "instruction": step.instruction
        } for step in Recipe_Steps.query.filter_by(recipe_id = recipe.id)
    ]

def getContributor(recipe: Recipe) -> dict:
    contributor = Contributor.query.filter_by(id = recipe.contributor_id).first()
    return {
        "contributor_name": contributor.name,
        "contributor_bio": contributor.name
    }

def getFullRecipe(recipeById: Recipe) -> dict:
    c = getContributor(recipeById)
    return {
        "id": recipeById.id,
        "name": recipeById.name,
        "prep_time": recipeById.prep_time,
        "description": recipeById.description,
        "difficulty": recipeById.difficulty,
        "vegetarian": recipeById.vegetarian,
        "quantity": recipeById.quantity,
        "unit": recipeById.unit,
        "contributor_name": c["contributor_name"],
        "contributor_bio": c["contributor_bio"],
        "recipe_tags": getRecipeTags(recipeById),
        "recipe_ingredients": getRecipeIngredients(recipeById),
        "recipe_steps": getRecipeSteps(recipeById)
    }

def getAllRecipes() -> list[dict]:
    return list(map(getFullRecipe, Recipe.query.all()))

def getSkillById(id: int) -> Skill | None:
    return None

def getSkillDictionary(skillById: Skill) -> dict | None:
    return None

def getAllSkills() -> list[dict]:
    return None