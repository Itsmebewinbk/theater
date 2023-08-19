from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.cache import cache
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from Admin.models import CustomUser
from Theater.models import Theater, Screen, Movie, Show
from Customer.models import BookingRequest
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.settings import api_settings
import datetime
from Customer.tasks.task import send_email


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        usertype = serializers.CharField(read_only=True)
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "image",
            "mobile",
            "gender",
            "age",
            "password",
            "usertype",
        )

    def validate(self, data):
        data["usertype"] = "customer"
        return data

    def create(self, validated_data, **kwargs):
        return CustomUser.objects.create_user(**validated_data)


class TheaterRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "image",
            "mobile",
            "gender",
            "age",
            "password",
        )

    def validate(self, data):
        data["usertype"] = "theater"
        return data

    def create(self, validated_data, **kwargs):
        return CustomUser.objects.create_user(**validated_data)


class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        read_only_fields = ("approval",)
        fields = (
            "id",
            "theater_name",
            "city",
            "image",
            "email_id",
            "phone_number",
            "theater_status",
            "about",
            "approval",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["screens"] = sum(
            list(
                instance.theatreowned.all().values_list("entry_fee", flat=True)
            )
        )

        return representation

    def create(self, validated_data):
        user = self.context["request"].user
        return Theater.objects.create(**validated_data, owner=user)


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ("id", "screen_name", "entry_fee", "total_seats")

    def validate(self, data):
        user = self.context["request"].user
        theater = Theater.objects.get(id=self.context["theater_id"])
        screen = [
            screens.screen_name
            for screens in Screen.objects.filter(
                theater__id=self.context["theater_id"]
            )
        ]
        if theater.owner != user:
            raise serializers.ValidationError("Not authorized")
        if theater.approval != True:
            raise serializers.ValidationError("theater not approved")
        if data.get("screen_name") in screen:
            raise serializers.ValidationError("screen_name already exists")
        return data

    def create(self, validated_data):
        theater_id = self.context.get("theater_id")
        return Screen.objects.create(theater_id=theater_id, **validated_data)


class SpecificScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ("id", "screen_name", "entry_fee", "total_seats")

    def validate(self, data):
        screen_id = self.context.get("screen_id")
        screen = [
            screens.screen_name
            for screens in Screen.objects.filter(id=screen_id)
        ]
        if data.get("screen_name") in screen:
            raise serializers.ValidationError("screen_name already exists")
        return data

    def create(self, validated_data):
        screen_id = self.context.get("screen_id")
        return Screen.objects.create(id=screen_id, **validated_data)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "id",
            "poster",
            "movie_name",
            "play_time",
            "start_date",
            "end_date",
        )

    def validate(self, data):
        screen_id = self.context.get("screen_id")
        shows = Show.objects.filter(
            movie__screen__id=screen_id, play_time=data["play_time"]
        ).exclude(screen_status="cancelled")
        if data["start_date"] < datetime.date.today():
            raise serializers.ValidationError("Start Date Invalid")
        if data["end_date"] < data["start_date"]:
            raise serializers.ValidationError("End Date Invalid")
        for show in shows:
            if data["start_date"] <= show.date <= data["end_date"]:
                raise serializers.ValidationError("Movie already Streaming")
        return data

    def create(self, validated_data):
        screen_id = self.context["screen_id"]
        create_movie = Movie.objects.create(
            screen_id=screen_id, **validated_data
        )

        total_days = (create_movie.end_date - create_movie.start_date).days
        dates = [
            create_movie.start_date + datetime.timedelta(days=data)
            for data in range(total_days + 1)
        ]
        show = [
            Show(
                movie=create_movie,
                date=date1,
                play_time=create_movie.play_time,
                TotalBooking=0,
            )
            for date1 in dates
        ]
        shows = Show.objects.bulk_create(show)
        return shows


class DeleteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "id",
            "poster",
            "movie_name",
            "play_time",
            "start_date",
            "end_date",
        )


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ("id", "screen_status", "play_time", "date", "TotalBooking")


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "id",
            "poster",
            "movie_name",
            "play_time",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["theater_name"] = instance.screen.theater.theater_name
        return representation


class MovieDetailSerializer(serializers.ModelSerializer):
    theater_status = serializers.CharField(
        source="screen.theater.theater_status"
    )
    total_seats = serializers.IntegerField(source="screen.total_seats")
    screen_name = serializers.CharField(source="screen.screen_name")
    price = serializers.IntegerField(source="screen.entry_fee")

    class Meta:
        model = Movie
        fields = (
            "id",
            "poster",
            "movie_name",
            "play_time",
            "theater_status",
            "total_seats",
            "screen_name",
            "price",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["theater_name"] = instance.screen.theater.theater_name
        representation["location"] = instance.screen.theater.city
        return representation


class ShowdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = (
            "id",
            "date",
        )


# Source MethodField
# gitlab pipeline
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequest
        fields = ("occupancy",)

    def validate(self, data):
        show_id = self.context.get("show_id")
        user = self.context["request"].user
        booking = BookingRequest.objects.filter(show_id=show_id)
        screen = Screen.objects.get(movie__show__id=show_id)
        show = Show.objects.get(id=show_id)
        total_occupancy = data["occupancy"]
        if (
            BookingRequest.objects.filter(
                customer=user, show_id=show_id
            ).count()
            >= 5
        ):
            raise serializers.ValidationError("Booking Limit Reached")
        for datas in booking:
            total_occupancy += datas.occupancy
            seats_left = screen.total_seats - (
                total_occupancy - data["occupancy"]
            )
            if screen.total_seats >= total_occupancy:
                pass
            else:
                if (
                    screen.total_seats - (total_occupancy - data["occupancy"])
                    == 0
                ):
                    raise serializers.ValidationError("Seats filled")
                else:
                    raise serializers.ValidationError(
                        f"Seats Left: {seats_left}"
                    )
        if total_occupancy == 0:
            show.screen_status = "empty"
        elif total_occupancy == screen.total_seats:
            show.screen_status = "housefull"
        elif total_occupancy - 1 >= screen.total_seats // 2:
            show.screen_status = "almostfull"
        elif total_occupancy > 0:
            show.screen_status = "filling"
        show.TotalBooking = total_occupancy
        show.save()

        for shows in Show.objects.filter(id=show.id):
            if str(shows.date) == str(datetime.date.today()):
                # datetime.datetime.hour
                if (shows.play_time == "Morning") and str(
                    datetime.time(9)
                ) > str(datetime.datetime.now().strftime("%H:%M:%S")):
                    pass
                elif (shows.play_time == "Noon") and str(
                    datetime.time(13)
                ) > str(datetime.datetime.now().strftime("%H:%M:%S")):
                    pass
                elif (shows.play_time == "1st") and str(
                    datetime.time(17)
                ) > str(datetime.datetime.now().strftime("%H:%M:%S")):
                    pass
                elif (shows.play_time == "2nd") and str(
                    datetime.time(21)
                ) > str(datetime.datetime.now().strftime("%H:%M:%S")):
                    pass
                else:
                    raise serializers.ValidationError(
                        "Movie already streaming"
                    )
            elif str(shows.date) < str(datetime.date.today()):
                raise serializers.ValidationError("Show expired")

        return data

    def create(self, validated_data):
        show_id = self.context.get("show_id")
        user = self.context["request"].user
        show = Show.objects.get(id=show_id)
        screen = Screen.objects.get(movie__show__id=show_id)
        validated_data["play_time"] = show.play_time
        validated_data["customer"] = user
        validated_data["screen"] = screen
        validated_data["show"] = show
        send_email.delay(id)
        return BookingRequest.objects.create(show_id=show_id, **validated_data)


class BookingListSerializer(serializers.ModelSerializer):
    date = serializers.CharField(source="show.date")
    movie_name = serializers.CharField(source="show.movie.movie_name")

    class Meta:
        model = BookingRequest
        fields = ("id", "movie_name", "occupancy", "date")


class AdminApprovalSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = (
            "id",
            "theater_name",
            "city",
            "image",
            "email_id",
            "phone_number",
            "theater_status",
            "about",
            "approval",
        )

    def update(self, instance, validated_data):
        instance.approval = True
        instance.save()
        return instance
