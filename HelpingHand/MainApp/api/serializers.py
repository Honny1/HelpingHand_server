from rest_framework.serializers import ModelSerializer

from MainApp.models import User, Device, Configuration, Day


class DaySerializer(ModelSerializer):
    class Meta:
        model = Day
        fields = ("name",)


class ConfigSerializer(ModelSerializer):
    day = DaySerializer(many=True, read_only=True)

    class Meta:
        model = Configuration
        fields = "__all__"


class DeviceSerializer(ModelSerializer):
    configuration = ConfigSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = "__all__"


class UserSerializer(ModelSerializer):
    device = DeviceSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("username","email","device")
