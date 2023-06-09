from rest_framework import serializers

from movies.models import (
    Movie,
    Review,
    Rating,
    RatingStar,
    Actor,
    Director,
    Category,
    Genre,
    MovieFrames,
)


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ("id", "name", "age", "description")


class ActorImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ("id", "image")


class ActorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ("id", "name", "image")


class ActorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ("id", "name", "age", "image", "description")


class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        exclude = ("image",)


class DirectorImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = ("id", "image",)


class DirectorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = ("id", "name", "image")


class DirectorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = ("id", "name", "age", "image", "description")


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="first_name", read_only=True
    )
    star = serializers.SlugRelatedField(
        slug_field="value", read_only=True
    )

    class Meta:
        model = Rating
        fields = ("user", "star")


class RatingCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    star = serializers.SlugRelatedField(
        slug_field="value", queryset=RatingStar.objects.all()
    )

    class Meta:
        model = Rating
        fields = ("user", "star", "movie")

    def create(self, validated_data):
        rating, created = Rating.objects.update_or_create(
            user=validated_data.get("user", None),
            movie=validated_data.get("movie", None),
            defaults={"star": validated_data.get("star")}
        )

        return rating


class FilterReviewListSerializer(serializers.ListSerializer):
    """Comment filter, only parents"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super(FilterReviewListSerializer, self).to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Recursive children output"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="first_name", read_only=True
    )
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("id", "user", "text", "children")


class ReviewCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="first_name", read_only=True
    )

    def validate(self, attrs):
        data = super(ReviewCreateSerializer, self).validate(attrs=attrs)
        if attrs["parent"]:
            if (
                attrs["parent"].user.email
                == self.context["request"].user.email
            ):
                raise serializers.ValidationError(
                    {"message": "You can't comment your reviews"}
                )
        return data

    class Meta:
        model = Review
        fields = "__all__"


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("name",)


class GenreCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ("name",)


class MovieFramesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieFrames
        fields = ("id", "title", "movies", "image")


class MovieFramesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieFrames
        fields = ("id", "image")


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        exclude = ("poster",)


class MoviePosterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ("id", "poster")


class MovieListSerializer(serializers.ModelSerializer):
    film_rating = RatingSerializer(many=True)
    average_rating = serializers.DecimalField(
        max_digits=3, decimal_places=1, read_only=True, coerce_to_string=False
    )

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "tagline",
            "film_rating",
            "average_rating",
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="name", read_only=True
    )
    genres = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=True
    )
    directors = DirectorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    film_rating = RatingSerializer(many=True)
    average_rating = serializers.DecimalField(
        max_digits=3, decimal_places=1, read_only=True, coerce_to_string=False
    )
    reviews = ReviewSerializer(many=True)
    film_shots = MovieFramesListSerializer(many=True)
    budget = serializers.SerializerMethodField()
    fees_in_the_usa = serializers.SerializerMethodField()
    fees_in_the_world = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "tagline",
            "poster",
            "film_shots",
            "year_of_release",
            "country",
            "category",
            "genres",
            "directors",
            "actors",
            "world_premiere",
            "budget",
            "fees_in_the_usa",
            "fees_in_the_world",
            "description",
            "film_rating",
            "average_rating",
            "reviews"
        )

    @staticmethod
    def get_budget(obj):
        budget = obj.budget
        formatted_budget = f"${budget}"
        return formatted_budget

    @staticmethod
    def get_fees_in_the_usa(obj):
        fees_in_the_usa = obj.fees_in_the_usa
        formatted_fees_in_the_usa = f"${fees_in_the_usa}"
        return formatted_fees_in_the_usa

    @staticmethod
    def get_fees_in_the_world(obj):
        fees_in_the_world = obj.fees_in_the_world
        formatted_fees_in_the_world = f"${fees_in_the_world}"
        return formatted_fees_in_the_world
