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
        fields = "__all__"


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
        fields = "__all__"


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
    user = serializers.SlugRelatedField(
        slug_field="first_name", read_only=True
    )
    star = serializers.SlugRelatedField(
        slug_field="value", queryset=RatingStar.objects.all()
    )

    class Meta:
        model = Rating
        fields = ("user", "star", "movie")

    def create(self, validated_data):
        rating, created = Rating.objects.update_or_create(
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
        fields = ("title", "image", "movies")


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"


class MovieListSerializer(serializers.ModelSerializer):
    film_rating = RatingSerializer(many=True)

    class Meta:
        model = Movie
        fields = ("id", "title", "tagline", "category", "film_rating")


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
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "tagline",
            "poster",
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
            "film_rating",
            "reviews"
        )
