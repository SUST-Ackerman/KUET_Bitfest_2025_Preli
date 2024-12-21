---

# API Documentation

This API provides endpoints for managing ingredients and recipes, as well as interacting with a chatbot that suggests recipes.


### 
Endpoints:

---

### 1. **Get All Ingredients**

- **Route**: `api/ingredients/`
- **Method**: `GET`
- **Description**: Fetches a list of all ingredients.

#### Sample Response:

```json
[
  {
    "id": 1,
    "name": "Tomato",
    "quantity": 2,
    "unit": "kg",
    "created_at": "2024-12-20T10:00:00Z",
    "updated_at": "2024-12-20T10:00:00Z"
  },
  {
    "id": 2,
    "name": "Onion",
    "quantity": 1,
    "unit": "kg",
    "created_at": "2024-12-20T10:05:00Z",
    "updated_at": "2024-12-20T10:05:00Z"
  }
]
```

---

### 2. **Get Ingredient by Name**

- **Route**: `api/ingredients/<name>/`
- **Method**: `GET`
- **Description**: Fetches a single ingredient by its name.

#### Sample Response: `api/ingredients/Tomato`

```json
{
  "id": 1,
  "name": "tomato",
  "quantity": 2,
  "unit": "kg",
  "created_at": "2024-12-20T10:00:00Z",
  "updated_at": "2024-12-20T10:00:00Z"
}
```

---

### 3. **Create a New Ingredient**

- **Route**: `api/ingredients/`
- **Method**: `POST`
- **Description**: Creates a new ingredient.

#### Sample Payload:

```json
{
  "name": "Garlic",
  "quantity": 0.5,
  "unit": "kg"
}
```

#### Sample Response:

```json
{
  "id": 3,
  "name": "Garlic",
  "quantity": 0.5,
  "unit": "kg",
  "created_at": "2024-12-21T12:00:00Z",
  "updated_at": "2024-12-21T12:00:00Z"
}
```

---

### 4. **Create a Recipe**

- **Route**: `api/recipes/add/`
- **Method**: `POST`
- **Description**: Creates a new recipe by providing recipe details in a text format.

#### Sample Payload:

```json
{
  "text": "Tomato Soup: 2 tomatoes, 1 onion, salt; Steps: Cut vegetables, Boil water, Blend ingredients."
}
```

#### Sample Response:

```json
{
  "recipe": "Recipe Name: Tomato Soup; Ingredients: 2 tomatoes, 1 onion, salt; Steps: Cut vegetables, Boil water, Blend ingredients."
}
```

---

### 5. **Get a Recipe**

- **Route**: `api/recipes/get/`
- **Method**: `POST`
- **Description**: Retrieves a recipe by name.

#### Sample Query: 

```json
{
  "name": "Tomato Soup"
}
```

#### Sample Response:

```json
{
  "recipe": "Recipe Name: Tomato Soup; Ingredients: 2 tomatoes, 1 onion, salt; Steps: Cut vegetables, Boil water, Blend ingredients."
}
```

---

### 6. **Chatbot for Recipe Suggestion**

- **Route**: `api/chatbot/`
- **Method**: `POST`
- **Description**: Interacts with the chatbot to suggest recipes based on the provided prompt.

#### Sample Payload:

```json
{
  "prompt": "Quick dinner with chicken and rice"
}
```

#### Sample Response (Styled HTML):

```html
<html>
<head>
  <style>
    /* Styles for recipe card */
  </style>
</head>
<body>
  <div class="form-container">
    <form method="post" action="">
      <input type="hidden" name="csrfmiddlewaretoken" value="CSRF_TOKEN">
      <textarea name="prompt" placeholder="Enter your prompt here..."></textarea>
      <button type="submit">Submit</button>
    </form>
  </div>
  <div class="recipe-card">
    Recipe Name: Chicken Rice; Ingredients: 2 chicken breasts, 1 cup rice, spices; Steps: Cook chicken, Boil rice, Combine.
  </div>
</body>
</html>
```

---

## Models

### Ingredient

- **Fields**:
  - `name`: The name of the ingredient (unique).
  - `quantity`: The quantity of the ingredient.
  - `unit`: The unit of measurement for the ingredient (e.g., kg, cup).
  - `created_at`: Timestamp when the ingredient was created.
  - `updated_at`: Timestamp when the ingredient was last updated.

### Recipe

- **Fields**:
  - `name`: The name of the recipe.
  - `ingredients`: A list of ingredients required for the recipe.
  - `steps`: The steps to prepare the recipe.

---

## Notes

- All date and time values follow the ISO 8601 format.
- The **CSRF token** is required for the POST request when interacting with the chatbot.

---

This README provides a structured overview of the API and its usage, covering routes, methods, sample responses, and payloads. You can adjust this documentation based on the exact behavior of your endpoints or any changes in the API.
