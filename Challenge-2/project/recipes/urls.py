from django.urls import path

from recipes.views import IngredientListCreateView, IngredientDetailView, RecipeCreateAPIView, RecipeRetrieveAPIView, \
    ChatbotAPIView

app_name = 'recipes'

urlpatterns = [
    path('ingredients/', IngredientListCreateView.as_view(), name='ingredients'),
    path('ingredients/<str:name>/', IngredientDetailView.as_view(), name='ingredient'),
    path('recipes/add/', RecipeCreateAPIView.as_view(), name='add-recipe'),
    path('recipes/get/', RecipeRetrieveAPIView.as_view(), name='get-recipe'),
    path('chatbot/', ChatbotAPIView.as_view(), name='chatbot'),
]
