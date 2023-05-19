from django.contrib import admin
from django import forms

from django.utils.safestring import mark_safe

from movies.models import (
    Category,
    Actor,
    Director,
    Genre,
    Movie,
    MovieFrames,
    RatingStar,
    Rating,
    Review,
)

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = "__all__"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    list_display_links = ("name", )
    search_fields = ("name",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image")
    search_fields = ("name",)
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='50' height='60'"
        )

    get_image.short_description = "Image"


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("name", "age",)
    search_fields = ("name",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='50' height='60'"
        )

    get_image.short_description = "Image"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ("user", )


class MovieFramesInline(admin.TabularInline):
    model = MovieFrames
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='100' height='130'"
        )

    get_image.short_description = "Movie episodes"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "year_of_release",
        "country",
        "world_premiere",
        "draft",
    )
    list_filter = ("category", "year_of_release", "country",)
    search_fields = ("title", "category__name")
    inlines = [MovieFramesInline, ReviewInline]
    save_on_top = True
    list_editable = ("draft", )
    actions = ["publish", "unpublish"]
    form = MovieAdminForm
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"),),
        }),
        (None, {
            "fields": (("directors", "actors", "genres", "category"),)
        }),
        (None, {
            "fields": (("year_of_release", "world_premiere", "country"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_the_usa", "fees_in_the_world"),)
        }),
        (None, {
            "fields": (("draft", ),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.poster.url} width='100' height='130'"
        )

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 record was updating"
        else:
            message_bit = f"{row_update} records were updating"
        self.message_user(request, f"{message_bit}")

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 record was updating"
        else:
            message_bit = f"{row_update} records were updating"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Publish"
    publish.allowed_permissions = ("change",)

    unpublish.short_description = "Stop the publication"
    unpublish.allowed_permissions = ("change",)

    get_image.short_description = "Poster"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "parent", "movie")
    readonly_fields = ("user",)


@admin.register(MovieFrames)
class MovieFramesAdmin(admin.ModelAdmin):
    list_display = ("title", "movies", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='50' height='60'"
        )

    get_image.short_description = "Image"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("movie", "star")


admin.site.register(RatingStar)

admin.site.site_title = "Django Movies API"
admin.site.site_header = "Django Movies API"
