from rest_framework import generics
from rest_framework.response import Response
from django.http import HttpResponse
from django.middleware.csrf import get_token


from recipes.gemini import Gemini
from recipes.models import Ingredient
from recipes.serializers import IngredientSerializer, RecipeCreateSerializer, RecipeRetrieveSerializer, \
    ChatbotSerializer


# Ingredient Views
class IngredientListCreateView(generics.ListCreateAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    lookup_field = 'name'
    lookup_url_kwarg = 'name'

    def get_object(self):
        name = self.kwargs.get(self.lookup_url_kwarg).lower()
        return self.queryset.filter(name__iexact=name).first()


class RecipeCreateAPIView(generics.CreateAPIView):
    serializer_class = RecipeCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prompt = f'''{serializer.validated_data['text']}
        
        
Convert the above recipe in one line, strictly in the following format:
Recipe Name: [name]; Ingredients: [ingredient1-quantity, ingredient2-quantity, ...]; Steps: [step1, step2, ...].
Ensure no additional explanation, and keep it concise.
        '''

        response = Gemini().generate_response(prompt)
        Gemini().add_recipe(response)
        return Response(response)


class RecipeRetrieveAPIView(generics.GenericAPIView):
    serializer_class = RecipeRetrieveSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = Gemini().get_recipe(serializer.validated_data['name'])

        return Response(response)


class ChatbotAPIView(generics.GenericAPIView):
    serializer_class = ChatbotSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = Gemini().suggest_recipe(serializer.validated_data['prompt'])

        styled_html_response = self.format_response_html(response)

        # Return as an HTML response
        return HttpResponse(styled_html_response, content_type="text/html")

    def format_response_html(self, raw_response):
        # Parse the raw response
        try:
            lines = raw_response.split("\n")
            name_line = lines[0].replace("Recipe Name: ", "")

            raw_response = raw_response.replace("\n", "<br>")

            # Create styled HTML
            html_response = (
                f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            max-width: 600px;
                            margin: 20px auto;
                            padding: 20px;
                            background-color: #f9f9f9;
                        }}
                        .recipe-card {{
                            border: 1px solid #ccc;
                            border-radius: 8px;
                            padding: 20px;
                            background-color: #fff;
                        }}
                        h3 {{
                            color: #333;
                            text-align: center;
                        }}
                        h4 {{
                            color: #555;
                            margin-top: 20px;
                        }}
                        ul {{
                            list-style: disc;
                            padding-left: 20px;
                            color: #333;
                        }}
                        ol {{
                            list-style: decimal;
                            padding-left: 20px;
                            color: #333;
                        }}
                        .form-container {{
                            margin-top: 20px;
                        }}
                        textarea {{
                            width: 100%;
                            height: 100px;
                            margin-bottom: 10px;
                        }}
                        button {{
                            padding: 10px 20px;
                            background-color: #007BFF;
                            color: #fff;
                            border: none;
                            border-radius: 4px;
                            cursor: pointer;
                        }}
                        button:hover {{
                            background-color: #0056b3;
                        }}
                    </style>
                </head>
                <body>
                <div class="form-container">
                        <form method="post" action="">
                            <input type="hidden" name="csrfmiddlewaretoken" value="{get_token(self.request)}">
                            <textarea name="prompt" placeholder="Enter your prompt here..."></textarea>
                            <button type="submit">Submit</button>
                        </form>
                    </div>
                    <div class="recipe-card">
                        {raw_response}
                    </div>
                    
                </body>
                </html>
                """
            )
            return html_response
        except Exception as e:
            return f"<p style='color: red;'>{raw_response}</p>"
