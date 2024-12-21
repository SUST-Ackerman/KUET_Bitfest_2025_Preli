from rest_framework import serializers

from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

    def create(self, validated_data):
        validated_data['name'] = validated_data['name'].lower()
        return Ingredient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['name'] = validated_data['name'].lower()
        return super().update(instance, validated_data)


class RecipeCreateSerializer(serializers.Serializer):
    text = serializers.CharField(style={'base_template': 'textarea.html'})


class RecipeRetrieveSerializer(serializers.Serializer):
    name = serializers.CharField()


class ChatbotSerializer(serializers.Serializer):
    prompt = serializers.CharField(style={'base_template': 'textarea.html'})
